import importlib
import traceback
import typing
import io
import sys
import enum
import json
import inspect
from IPython import get_ipython
from IPython.display import display, DisplayHandle
from IPython.core.displaypub import CapturingDisplayPublisher
from IPython.core.displayhook import CapturingDisplayHook
from ipykernel.comm.comm import Comm
from ipykernel.comm.manager import CommManager


class _PseudoWriter(io.TextIOBase):
    def __init__(self, comm: Comm, name: str) -> None:
        self._comm = comm
        self._name = name

    def writable(self) -> bool:
        return True

    def write(self, message: str) -> int:
        self._comm.send({
            'type': 'output',
            'output': {
                'output_type': 'stream',
                'name': self._name,
                'text': message
            }
        })

        return len(message)


class _DummyList(list):
    def __init__(self, comm: Comm) -> None:
        super().__init__()
        self._comm = comm

    def append(self, item: typing.Any) -> None:
        if isinstance(item, typing.Sequence):
            msg = {
                'output_type': 'display_data',
                'data': item[0],
                'metadata': item[1]
            }
        else:
            msg = item
        self._comm.send({
            'type': 'output',
            'output': msg
        })


class Biyam:
    @staticmethod
    def _native_to_biyam_type(tp: typing.Type) -> typing.Any:
        if tp is bool:
            return 'Check'
        elif tp in (int, float):
            return 'Number'
        elif tp is str:
            return 'String'
        elif issubclass(tp, enum.Enum):
            return {k: v.value for k, v in tp.__members__.items()}
        return None

    @staticmethod
    def procedure(ret_type: typing.Optional[typing.Type]=None,
                  args: typing.Sequence[typing.Dict[str, typing.Any]]=(),
                  inline: typing.Optional[bool]=None,
                  no_func: bool=False,
                  no_proc: bool=False)\
            -> typing.Callable[[typing.Callable], typing.Callable]:
        def decorator(fn: typing.Callable) -> typing.Callable:
            meta: typing.Dict[str, typing.Any] = {}
            no_func_ = no_func
            ret_type_ = ret_type

            if ret_type is None:
                if 'return' in fn.__annotations__:
                    if fn.__annotations__['return'] is None:
                        no_func_ = True
                    ret_type_ = fn.__annotations__['return']

            if ret_type_ is not None:
                rtp = Biyam._native_to_biyam_type(ret_type_)
                if rtp is not None:
                    meta['ret_type'] = rtp

            meta['args'] = list(args)
            for param in inspect.signature(fn).parameters:
                if all(arg['name'] != param for arg in args):
                    spec = {'name': param}
                    tp_ = fn.__annotations__.get(param, None)
                    if param in fn.__annotations__ and tp_:
                        spec['type'] = Biyam._native_to_biyam_type(tp_)
                    meta['args'].append(spec)

            if inline is not None:
                meta['inline'] = inline
            meta['no_func'] = no_func_
            meta['no_proc'] = no_proc

            setattr(fn, '_biyam_meta_', meta)
            return fn

        return decorator

    @staticmethod
    def _gather_procedures(mod_name: str) -> typing.Dict[str, typing.Any]:
        mod = importlib.import_module(mod_name)

        return {
                k: getattr(v, '_biyam_meta_')
                for k in dir(mod) if not k.startswith('_')
                for v in (getattr(mod, k, None),)
                if hasattr(v, '_biyam_meta_') and hasattr(v, '__call__')
        }

    @staticmethod
    def _comm_target(comm: Comm, msg: typing.Dict[str, typing.Any]) -> None:
        @comm.on_msg  # type: ignore
        def on_msg(msg: typing.Dict[str, typing.Any]) -> None:
            stdout_ = sys.stdout
            stderr_ = sys.stderr
            displayhook_ = sys.displayhook
            shell = get_ipython()
            display_pub_ = shell.display_pub if shell else None

            try:
                sys.stdout = typing.cast(typing.Any,
                                         _PseudoWriter(comm, 'stdout'))
                sys.stderr = typing.cast(typing.Any,
                                         _PseudoWriter(comm, 'stderr'))
                if shell:
                    outputs = _DummyList(comm)
                    shell.display_pub = CapturingDisplayPublisher()
                    shell.display_pub.outputs = outputs
                    sys.displayhook = CapturingDisplayHook(shell, outputs)

                mod_name = msg['content']['data'].get('mod', '__main__')

                mod = importlib.import_module(mod_name)
                fn_ = getattr(mod, msg['content']['data'].get('fn', 'main'))
                ret = fn_(**msg['content']['data'].get('args', {}))

                comm.send({
                    'type': 'result',
                    'ok': True,
                    'ret': ret
                })
            except Exception:
                traceback.print_exc()
                comm.send({
                    'type': 'result',
                    'ok': False
                })
            finally:
                sys.stdout = stdout_
                sys.stderr = stderr_
                sys.displayhook = displayhook_
                if shell:
                    shell.display_pub = display_pub_

    def __init__(self, *mods: str) -> None:
        self._info = {
            'procedures': {
                mod: Biyam._gather_procedures(mod)
                for mod in mods
            }
        }

    def _ipython_display_(self, **kwargs: typing.Any)\
            -> typing.Optional[DisplayHandle]:
        return display({
            'text/plain': "Biyam Workspace",
            'application/x.biyam+json': self._info,
        }, raw=True, **kwargs)

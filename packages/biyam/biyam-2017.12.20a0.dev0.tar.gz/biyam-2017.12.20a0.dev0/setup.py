from setuptools import setup


setup(
        name="biyam",
        version="2017.12.20a0.dev0",
        packages=["biyam"],
        package_data={'biyam': ['*.xml', 'static/*']},
        url='https://github.com/gwangyi/biyam',
        license='MIT',
        author='Sungkwang Lee',
        author_email='gwangyi.kr@gmail.com',
        description='Blockly w/ Python on Jupyter Notebook',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
        ],
        install_requires=['jupyter']
)

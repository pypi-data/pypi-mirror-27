from setuptools import setup, find_packages

setup(
    name='jordan',
    version='0.0.1',
    install_requires=[
            'cython'
    ],
    author='PLAIDLab',
    url='https://github.com/plaidlab/jordan',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.4'
)

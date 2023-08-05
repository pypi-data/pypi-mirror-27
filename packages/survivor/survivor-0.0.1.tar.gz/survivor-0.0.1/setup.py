from setuptools import setup, find_packages

setup(
    name='survivor',
    version='0.0.1',
    description='Toolkit for survival analysis on patient data',
    url='https://github.com/n-s-f/survivor',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
)

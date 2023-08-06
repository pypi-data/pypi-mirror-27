#!/usr/bin/env python3

from setuptools import setup, find_packages

readme = open('README.rst').read()

with open('cjmls.py') as f:
    for line in f:
        if line.startswith('__version__ = '):
            version = eval(line.strip().split(' = ')[-1])
            break

if version is None:
    raise Exception("version not found")

setup(
    name='cjmls',
    version=version,
    description='Python wrapper for cjmls.',
    long_description=readme,
    author='Al Johri',
    author_email='al.johri@gmail.com',
    url='https://github.com/AlJohri/cjmls',
    license='MIT',
    py_modules=['cjmls'],
    install_requires=['requests',],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ]
)

#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

import jzqt


setup(
    name='jzqt',
    version=jzqt.__version__,
    packages=['jzqt'],
    author='JZQT',
    author_email='561484726@qq.com',
    url="https://github.com/JZQT/jzqt",
    description="Python tools library",
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)

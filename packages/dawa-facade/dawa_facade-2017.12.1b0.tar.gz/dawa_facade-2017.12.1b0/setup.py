#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""setup.py
Copyright 2017 Martin Storgaard Dieu under The MIT License

Written by Martin Storgaard Dieu <martin@storgaarddieu.com>, november 2017
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re

reqs = ['requests>=2.5', 'ijson==2.3']

tests_requires = ['requests_mock']

with open('dawa_facade/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='dawa_facade',
    version=version,
    description='Python client for Danmarks Adressers Web API',
    author_email="martin@storgaarddieu.com",
    author="Martin Storgaard Dieu",
    url="https://github.com/YnkDK/Dawa-Facade",
    packages=['dawa_facade'],
    license='MIT',
    install_requires=reqs,
    tests_requires=tests_requires,
    keywords=['dawa', 'Danmarks Adressers Web API', 'addresses', 'adresser', 'denmark', 'danmark'],
    download_url='https://github.com/YnkDK/Dawa-Facade/archive/2017.12.1.b1.tar.gz'
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018, Mark Bundgus
import os

from setuptools import setup

import scabbard

setup(
    name="scabbard",
    version=scabbard.version,
    license="BSD 3-Clause License",
    description="Pythonic client for Sabre Dev Studio REST APIs",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       "README.rst")).read(),
    author="Mark Bundgus",
    author_email="bundgus@gmail.com",
    url="https://github.com/bundgus/scabbard",
    packages=["scabbard"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        "bravado >= 9.2.2",
        "pytz",
        "iso8601",
        "requests >= 2.18",
    ],
    include_package_data=True,
)

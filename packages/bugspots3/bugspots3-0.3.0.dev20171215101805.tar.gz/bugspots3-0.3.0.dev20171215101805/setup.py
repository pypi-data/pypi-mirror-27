#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 textwidth=79

from setuptools import setup
from setuptools import find_packages

import bugspots3

setup(
    name="bugspots3",
    version=bugspots3.__version__,
    description=bugspots3.__doc__,
    author=bugspots3.__author__,
    author_email="support@gitmate.io",
    url="https://gitlab.com/gitmate/bugspots3",
    py_modules=["bugspots3"],
    scripts=["bugspots"],
    license=bugspots3.__license__,
    packages=find_packages(exclude=["build.*", "dist"]),
    include_package_data=True,
    platforms="Unix",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"])

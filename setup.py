#!/usr/bin/env python

#
# @author Ari Setiawan
# @create 15.10-2023 23:39
# @github https://github.com/hxAri/Yutiriti
#
# Yūtiriti Copyright (c) 2022 - Ari Setiawan <hxari@proton.me>
# Yūtiriti Licence under GNU General Public Licence v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#


from setuptools import find_packages as finder, setup


#[setup.reader( Str fname )]: Str
def reader( fname:str ) -> str:
    fread = ""
    with open( fname, "r" ) as fopen:
        fread = fopen.read()
        fopen.close()
    return fread


setup(
    name="yutiriti",
    version="1.0.0",
    author="Ari Setiawan (hxAri)",
    author_email="hxari@proton.me",
    maintainer="Ari Setiawan (hxAri)",
    maintainer_email="hxari@proton.me",
    description="",
    packages=['yutiriti'],
    package_dir={ "": "src" },
    provides_extra=reader( "requirements.txt" ).split( "\x0a" ),
    long_description=reader( "README.md" ),
    url="https://github.com/hxAri/Yutiriti",
    download_url="https://github.com/hxAri/Yutiriti/archive/refs/heads/main.zip",
    license="GNU General Public Licence v3",
    classifiers=[
        "Environment :: CLI Environment",
        "Intended Audience :: Developers",
        "Licence :: GNU",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet :: Command Line Interface",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only"
    ]
)


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


from setuptools import setup
from yutiriti.file import File
from yutiriti.config import *


setup(
	name=TITLE,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	description=DESCRIPTION,
	requires=File.line( "requirements.txt" ),
	long_description=File.read( "README.md" ),
	url=REPOSITORY,
	license=LICENSE,
	classifiers=[
		"Environment :: CLI Environment",
		"Intended Audience :: Developers",
		"Licence :: {}".format( LICENSE ),
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


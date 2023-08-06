#!/usr/bin/env python
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from setuptools import setup, find_packages
import os
import glob
import sys
import re


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

args = {}

dist = setup(
    name='twister-game',
    version='2.0',
    description='Twister',
    long_description=read('README'),
    author='Albert Cervera i Areny',
    author_email='albert@nan-tic.com',
    url='http://bitbucket.org/albertnan/twister',
    download_url='http://bitbucket.org/albertnan/twister',
    keywords='twister game',
    scripts=['twister.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment',
        ],
    platforms='any',
    license='GPL-3',
    install_requires=[
        "blessings",
        ],
    zip_safe=False,
    **args
    )

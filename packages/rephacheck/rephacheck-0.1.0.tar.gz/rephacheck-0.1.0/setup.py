#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from io import open
from os import path
from setuptools import find_packages, setup
from re import M, search

here = path.abspath(path.dirname(__file__))


def read(*parts):
    with open(path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                           version_file, M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='rephacheck',
    version=find_version("src", "rephacheck", "__init__.py"),
    description='Health check for PostgreSQL cluster managed by repmgr',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    keywords='haproxy healthcheck postgresql repmgr',
    author='Nicolas KAROLAK',
    author_email='nicolas@karolak.fr',
    url='https://gitlab.com/NicolasKAROLAK/rephacheck',
    license='Public Domain',
    package_dir={"": "src"},
    packages=find_packages('src'),
    package_data={
        'rephacheck': ['*.json'],
    },
    python_requires='>=2.7',
    install_requires=['future', 'psycopg2'],
    entry_points={
        "console_scripts": [
            "rephacheck=rephacheck.server:run",
        ],
    },
)

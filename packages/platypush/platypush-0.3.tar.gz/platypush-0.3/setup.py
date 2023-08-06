#!/usr/bin/env python

import errno
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def pkg_files(dir):
    paths = []
    for (path, dirs, files) in os.walk(dir):
        for file in files:
            paths.append(os.path.join('..', path, file))
    return paths

def create_etc_dir():
    path = '/etc/platypush'
    try:
        os.makedirs(path)
    except OSError as e:
        if isinstance(e, PermissionError):
            print('WARNING: Could not create /etc/platypush')
        elif e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

plugins = pkg_files('platypush/plugins')
backend = pkg_files('platypush/backend')
create_etc_dir()

setup(
    name = "platypush",
    version = "0.3",
    author = "Fabio Manganiello",
    author_email = "info@fabiomanganiello.com",
    description = ("Platypush service"),
    license = "MIT",
    python_requires = '>= 3',
    keywords = "pushbullet notifications automation",
    url = "https://github.com/BlackLight/platypush",
    # packages = ['platypush'],
    packages = find_packages(),
    # package_data = {'': plugins},
    scripts = ['platypush/bin/pusher'],
    entry_points = {
        'console_scripts': [
            'platypush=platypush:main',
        ],
    },
    data_files = [
        ('/etc/platypush', ['platypush/config.example.yaml'])
    ],
    long_description = read('README.md'),
    classifiers = [
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
    ],
    install_requires = [
        'pyyaml',
        'websocket-client',
    ],
)


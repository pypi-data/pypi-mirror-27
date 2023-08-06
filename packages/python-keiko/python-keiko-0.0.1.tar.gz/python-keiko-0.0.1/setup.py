#!/usr/bin/env python

from distutils.core import setup

setup(
    name                    = 'python-keiko',
    version                 = '0.0.1',  # can't get from init.py before build
    description             = 'Lightweight MySQL client library',
    author                  = 'Ross McFarland',
    author_email            = 'ross@gmail.com',
    long_description        = 'Lightweight MySQL client library modeled '
                              'after MySQLdb, but really on the portions '
                              'Django relies upon',
    license                 = 'MIT',
    url                     = 'https://github.com/github/keiko',
)

#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup\
    ( name='rating_service'
    , version='1.0'
    , description='JSON-RPC service for storing and traking resource rating'
    , author='Sergey Nikitin'
    , author_email='nikitinsm@gmail.com'
    , url='https://github.com/nikitinsm/rating-service'
    , packages = find_packages('src')
    , package_dir = {'': 'src'}
    , include_package_data = True
    , install_requires =
      [ "gevent"
      , "gunicorn"
      , "json-rpc"
      , "redis"
      , "werkzeug"
      , "wtform"
      ]
    )
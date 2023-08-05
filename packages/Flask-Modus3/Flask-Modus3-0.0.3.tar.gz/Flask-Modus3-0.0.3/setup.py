#!/usr/bin/env python

"""
Flask-Reggie
------------

Quickly and Easily enable Regex Routes within your Flask Application

"""

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='Flask-Modus3',
    version='0.0.3',
    url='https://github.com/toChaim/flask-modus3',
    author='Rhys Elsmore and Chaim Finkelman',
    author_email='toChaim@gmail.com',
    description='Flask Method Overrides for python 2.7 and 3.6',
    long_description=open('README.rst').read() + '\n\n' +
        open('HISTORY.rst').read(),
    py_modules=['flask_modus3'],
    license=open('LICENSE').read(),
    package_data={'': ['LICENSE']},
    zip_safe=False,
    platforms='any',
    install_requires=[
        'setuptools',
        'Flask',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

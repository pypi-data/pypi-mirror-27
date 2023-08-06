#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='dojo',
    version='0.1.0',
    description='A framework for building and running your data platform.',
    author='Data Up',
    author_email='dojo@dataup.me',
    url='https://www.dataup.me/',
    packages=find_packages(exclude=['tests', '.cache', '.venv', '.git', 'dist']),
    install_requires=[
        'apache-beam[gcp]',
        'google-cloud-storage==1.2.0',
        'grpcio==1.4.0',
        'six==1.10.0',
        'stored',
        'click',
        'jsonschema',
        'python-dateutil',
    ],
    entry_points='''
        [console_scripts]
        dojo=dojo.cli:cli
    ''',
)

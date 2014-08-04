#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='graph',
    version='1.0',
    description="",
    author="arun",
    author_email='arun@ternup.com',
    url='',
    packages=find_packages(),
    package_data={'graph': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)

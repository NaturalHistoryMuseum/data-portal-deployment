#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '24/11/2017'.
"""

from setuptools import setup

setup(
    name='deployment',
    version='0.0.1',
    description='Deployment',
    author='Ben Scott',
    author_email='ben@benscott.co.uk',
    packages=[
        'deployment',
    ],
    py_modules=['deployment'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        deploy=deployment.cli:deploy
    ''',
)

#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='devnone',
    version='0.0.1',
    description='',
    long_description='',
    author='Eduardo Matos',
    author_email='eduardo.matos.silva@gmail.com',
    url='https://github.com/eduardo-matos/devnone',
    packages=[
        'devnone',
    ],
    include_package_data=True,
    install_requires=[
        'flask>=0.10.1'
    ],
    license='MIT',
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)

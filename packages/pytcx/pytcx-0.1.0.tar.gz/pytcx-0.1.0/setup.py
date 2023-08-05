#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://pytcx.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pytcx',
    version='0.1.0',
    description='GPX parsing for Python',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Karl Odie',
    author_email='karlodie@gmail.com',
    url='https://github.com/heoga/pytcx',
    py_modules=['pytcx'],
    include_package_data=True,
    install_requires=[
        'xmltodict',
    ],
    license='MIT',
    zip_safe=False,
    keywords='pytcx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

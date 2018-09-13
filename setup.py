#!/usr/bin/env python3

from setuptools import setup
import os

with open("README.rst") as readme:
    long_description = readme.read()

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'i2plib', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    keywords='i2p',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['i2plib'],
)

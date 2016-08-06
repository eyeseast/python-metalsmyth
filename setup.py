#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as f:
    readme = f.read()


requirements = [
    'python-frontmatter',
    'six'
]


VERSION = '0.1.6'


setup(
    name = 'metalsmyth',
    version = VERSION,
    description = 'Process a directory of files with frontmatter and middleware',
    long_description = readme,
    author = 'Chris Amico',
    author_email = 'eyeseast@gmail.com',
    url = 'https://github.com/eyeseast/python-metalsmyth',
    packages = ['metalsmyth', 'metalsmyth.plugins'],
    include_package_data = True,
    install_requires = requirements,
    license = 'MIT',
    zip_safe = False,
    keywords = 'frontmatter static-generator',
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
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='test',
)

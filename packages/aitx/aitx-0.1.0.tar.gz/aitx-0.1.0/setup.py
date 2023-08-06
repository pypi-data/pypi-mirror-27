#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import sys
import os

with open('README.md') as readme_file:
    readme = readme_file.read()

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='aitx',
    version='0.1.0',
    description="The toolbox for general ML projects",
    long_description=readme,
    author="Chia-Jung, Yang",
    author_email='jeroyang@gmail.com',
    url='https://github.com/jeroyang/aitx',
    packages=[
        'aitx',
    ],
    package_dir={'aitx':
                 'aitx'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='aitx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
)

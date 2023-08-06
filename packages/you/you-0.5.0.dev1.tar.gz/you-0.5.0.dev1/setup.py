#!/usr/bin/env python3
"""A setuptools based setup module.

Based on: <https://github.com/pypa/sampleproject>
"""

from setuptools import setup, find_packages
from codecs import open  # use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# read the package name and version
exec(open('you/version.py').read())

setup(
    name=locals().get('NAME'),
    version=locals().get('__version__'),
    description=locals().get('DESCRIPTION'),
    long_description=long_description,
    # keywords='sample setuptools development',

    url='https://github.com/soimort/you-get/tree/0.5/0.5',
    license='MIT',

    author='Mort Yao',
    author_email='soi@mort.ninja',

    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Desktop Environment',
        'Topic :: Internet',
        'Topic :: Multimedia',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    extras_require={
        # 'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },

    package_data={
        # 'sample': ['package_data.dat'],
    },

    entry_points={
        'console_scripts': [
            'you=you.main:main',
        ],
    },
)

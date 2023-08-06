#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

setup(
    name='crymon',
    version='2017.12.14',
    description='Routines for crystallography with single crystals',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/crymon',
    license='GPLv3',
    install_requires=[
        'cryio',
        'numpy',
    ],
    packages=[
        'crymon',
    ],
    ext_modules=[
        Extension(
            'crymon._crymon', [
                'src/crymonmodule.c',
                'src/ccp4.c',
            ],
        )
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

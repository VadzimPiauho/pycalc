#!/usr/bin/env python3

import setuptools

with open("README", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pycalc",
    version="0.1",
    author="Vadzim Pliauho",
    author_email="vadik_pl@outlook.com",
    description="Pure-python command-line calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VadzimPiauho/pycalc",
    packages=("pycalc",),
    entry_points={
        'console_scripts':
            ['pycalc = main:_main']
    },
)

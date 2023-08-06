#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


setup(
    name='ethereum-utils',
    version='0.6.2',
    description="""Common utility functions for ethereum codebases.""",
    long_description_markdown_filename='README.md',
    author='Piper Merriam',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/ethereum/eth-utils',
    include_package_data=True,
    install_requires=[],
    setup_requires=['setuptools-markdown'],
    py_modules=['eth_utils'],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

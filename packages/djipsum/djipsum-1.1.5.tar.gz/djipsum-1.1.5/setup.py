#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from djipsum import (__VERSION__, __AUTHOR__, __AUTHOR_EMAIL__)

setup(
    name="djipsum",
    packages=find_packages(exclude=["*.demo"]),
    version=__VERSION__,
    url="https://github.com/agusmakmun/djipsum/",
    download_url="https://github.com/agusmakmun/djipsum/tarball/v{}".format(__VERSION__),
    description="Django Lorem Ipsum Generator - Command plugin to generate (fake content data) for Django model.",
    long_description=open("README.rst").read(),
    license="MIT",
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    keywords=[
        "djipsum", "django fake content data",
        "django lorem ipsum generator",
        "django unitest tool"
    ],
    zip_safe=False,
    include_package_data=True,
    install_requires=["Django>=1.10.1", "Faker>=0.7.3"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Framework :: Django",
    ]
)

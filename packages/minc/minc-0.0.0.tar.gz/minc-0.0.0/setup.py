#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = []
test_requirements = []

setup(
    name="minc",
    version="0.0.0",
    description="MIscreaNt Cryptotool",
    long_description="MIscreaNt Cryptotool",
    author="Tony Arcieri",
    author_email="bascule@gmail.com",
    url="https://github.com/miscreant/minclib",
    packages=find_packages(exclude=["tests"]),
    package_dir={"minc": "minc"},
    include_package_data=True,
    install_requires=[],
    license="MIT license",
    zip_safe=False,
    keywords=["cryptography", "security", "signatures"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    test_suite="tests",
    tests_require=[]
)

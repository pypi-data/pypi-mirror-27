#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = []
test_requirements = []

setup(
    name="keyuri",
    version="0.0.0",
    description="A URI-based format for encoding cryptographic keys",
    long_description=(
        "KeyURI leverages the URI generic syntax defined in RFC 3986 to "
        "provide simple and succinct encodings of cryptographic keys, "
        "including public keys, private/secret keys, and encrypted secret "
        "keys with password-based key derivation"
    ),
    author="Tony Arcieri",
    author_email="bascule@gmail.com",
    url="https://github.com/miscreant/keyuri",
    packages=find_packages(exclude=["tests"]),
    package_dir={"keyuri": "keyuri"},
    include_package_data=True,
    install_requires=[],
    license="MIT license",
    zip_safe=False,
    keywords=["cryptography", "security"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    test_suite="tests",
    tests_require=[]
)

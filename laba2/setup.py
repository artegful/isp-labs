#!/usr/bin/env python

from platform import python_version_tuple

import setuptools


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if python_version_tuple()[0] < "3":
    raise ValueError("Error python version. Need python3 and more")

with open("README.md", "r") as fp:
    readme = fp.read()

setup(
    name="serializer",
    version="0.1.0",
    description="Serializer that uses different formats",
    author="Artegful",
    url="https://github.com/artegful/isp-labs/tree/master/laba2",
    license="MIT",
    setup_requires=["wheel"],
    install_requires=["pyyaml", "wheel"],
    packages=["serializer", "serializer.utility", "custom_json", "custom_yaml", "custom_pickle"],
    entry_points={"console_scripts": "convert=serializer.__main__:main"},
)

# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "tbs-sdk"
VERSION = "0.0.5"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="3blades API",
    author_email="",
    url="https://github.com/3Blades/python-sdk",
    download_url=f'https://github.com/3Blades/python-sdk/archive/{VERSION}.tar.gz',
    keywords=["3blades API", "Data Science"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
)

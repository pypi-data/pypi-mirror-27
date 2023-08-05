#!/usr/bin/env python3.5
# -------------------------------------------------------------------------
# Multi-Rotor Robot Design Team
# Missouri University of Science and Technology
# Fall 2017
# Christopher O'Toole
# -------------------------------------------------------------------------

from setuptools import find_packages
from setuptools import setup
from mrrdt_vision.__init__ import __version__

REQUIRED_PACKAGES = []
PACKAGE_NAME = 'mrrdt_vision'

setup(
    name=PACKAGE_NAME,
    version=__version__,
    install_requires = REQUIRED_PACKAGES,
    packages = find_packages(),
    include_package_data = True,
    description='%s %s' % (PACKAGE_NAME, __version__),
    url='https://github.com/MST-MRR/IARC-2018',
    author="Christopher O'Toole",
    author_email='cdocq9@mst.edu',
    license='MIT'
)
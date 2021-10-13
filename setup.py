#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="CTI-website-backend",
      version="0.9.0",
      description="API server for https://civictechindex.org",
      author="Hack for LA",
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "htmlcov"])
      )

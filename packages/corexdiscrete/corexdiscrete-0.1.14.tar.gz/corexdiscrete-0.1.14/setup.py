# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="corexdiscrete",
    version="0.1.14",
    description="Corex finds latent factors that explain the most correlation in discrete data.",
    license="MIT",
    author="Rob Brekelmans/Greg Ver Steeg",
    author_email="brekelma@usc.edu",
    packages=find_packages(),
    url='https://github.com/brekelma/corexdiscrete',
    download_url='https://github.com/brekelma/corexdiscrete',
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ], 
    entry_points = {
    'd3m.primitives': [
        'corex_discrete.CorexDiscrete = corexdiscrete.corex_discrete:CorexDiscrete',
    ],
    }
)

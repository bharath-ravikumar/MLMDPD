#!/usr/bin/env python

from setuptools import setup, find_packages

from codecs import open
from os import path

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup( name = "MLMDPD",
        version = "0.1.0",
        author = ["Bharath Ravikumar"],
        packages = find_packages(where="src"),
        package_dir={"":"src"},
        install_requires=[
            'numpy','scipy','pandas','scikit-learn==1.5.2','deap','networkx'
            ],
        entry_points={
            'console_scripts': [
                'MLMDPD=packages.run_MLMDPD:main'
                ]
            },
)


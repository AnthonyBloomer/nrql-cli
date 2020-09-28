#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must install Twine:
#   $ pip install -r requirements.txt

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.
NAME = 'nrql-cli'
DESCRIPTION = 'An interactive command line interface for querying NRQL data.'
URL = 'https://github.com/anthonybloomer/nrql-cli'
EMAIL = 'ant0@protonmail.ch'
AUTHOR = 'Anthony Bloomer'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = "1.0.3"
LICENSE = 'MIT'
REQUIRED = [
    'requests', 'colorful', 'halo', 'prompt_toolkit', 'pygments'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst')) as f:
    long_description = '\n' + f.read()

about = {'__version__': VERSION}


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["nrql"],
    entry_points={
        'console_scripts': ['nrql=nrql.cli:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)

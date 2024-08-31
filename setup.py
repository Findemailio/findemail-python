#!/usr/bin/env python3
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject

Extra supported commands are:
* gen, to generate the classes required for Telethon to run or docs
* pypi, to generate sdist, bdist_wheel, and push to PyPi
"""

import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

# Needed since we're importing local files
sys.path.insert(0, os.path.dirname(__file__))

class TempWorkDir:
    """
    Switches the working directory to be the one on which this file lives,
    while within the 'with' block.
    """
    def __init__(self, new=None):
        self.original = None
        self.new = new or str(Path(__file__).parent.resolve())

    def __enter__(self):
        # os.chdir does not work with Path in Python 3.5.x
        self.original = str(Path('.').resolve())
        os.makedirs(self.new, exist_ok=True)
        os.chdir(self.new)
        return self

    def __exit__(self, *args):
        os.chdir(self.original)


def main(argv):
    setup(
        name='findemail',
        version="1.0.0",
        description='findemail api library for Python 3',

        url='https://github.com/findemail/findemail-python',

        author='Findemailio',

        # See https://stackoverflow.com/a/40300957/4759433
        # -> https://www.python.org/dev/peps/pep-0345/#requires-python
        # -> http://setuptools.readthedocs.io/en/latest/setuptools.html
        python_requires='>=3.5',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',

            'Intended Audience :: Developers',
            'Topic :: Communications :: Chat',

            'License :: OSI Approved :: MIT License',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        keywords='findemail email api',
        packages=find_packages(),
        install_requires=['requests']
    )


if __name__ == '__main__':
    with TempWorkDir():
        main(sys.argv)

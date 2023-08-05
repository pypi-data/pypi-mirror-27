# -*- coding: utf-8 -*-
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '-s',
            '-ra',
            '--verbose',
            '--flake8',
            '--isort',
            '--cov-report=xml',
            '--cov-report=term-missing',
            '--cov=compander',
            '--junitxml=junit.xml',
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'compander', 'version.txt')) as f:
    VERSION = f.read().strip()

setup(
    name="compander",
    version=VERSION,
    license="MIT",
    description="Simple context manager for wrapping file compression and uncompression operations.",
    long_description=README,
    url="",
    keywords="python file compressor / uncompressor context bzip2 bz2 gzip gz",
    packages=find_packages(),
    py_modules=['compander'],
    cmdclass={'test': PyTest},
    tests_require=[
        'flake8==3.0.4',
        'pytest==3.0.3',
        'pytest-flake8==0.8.1',
        'pytest-isort==0.1.0',
        'pytest_bdd',
        'flake8-isort==2.0.1',
        'pytest-cov',
        'setuptools',
    ],
    install_requires=[
        'setuptools',
    ],
    dependency_links=[
    ],
    package_data={
        '': ['*.txt', '*.rst', '*.md', '*.json', '*.conf'],
    },
    classifiers=[
        # Development Status: 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

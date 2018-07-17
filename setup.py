# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os
import re


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


long_description = read('README.rst')


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='seeddms',
      version=find_version('seeddms', 'version.py'),
      description='SeedDMS cli',
      long_description=long_description,
      url='',
      author='John van Zantvoort',
      author_email='john@vanzantvoort.org',
      license='MIT',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Office/Business',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
      ],
      keywords='dms seeddms',
      packages=find_packages(exclude=['docs', 'docs-src', 'tests']),
      install_requires=[])

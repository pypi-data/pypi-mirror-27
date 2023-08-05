#from distutils.core import setup
from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()

setup(
      name='RepAlytics',
      version='1.0.0',
      description='A module for access to Teradata and Google Sheets',
      license='Automation for stuff at werk',
      long_description=long_description,
      classifiers=[
          'Programming Language :: Python :: 3.5'
    ],
      find_packages=find_packages,
      python_requires='>=3',
)
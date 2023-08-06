#!/usr/bin/python3
"""Setup
"""
from setuptools import find_packages
from distutils.core import setup

version = "0.0.1"

with open('README.rst') as f:
    long_description = f.read()

setup(name='ofxstatement-be-triodos',
      version=version,
      author="Bernard Butaye",
      author_email="",
      url="https://github.com/renardeau/ofxstatement-be-triodos",
      description=("ofxstatement plugin for parsing Belgian Triodos bank's CSV statements to OFX"),
      long_description=long_description,
      license="GPLv3",
      keywords=["ofx", "banking", "statement", "triodos", "csv"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          'ofxstatement':
          ['triodosbe = ofxstatement.plugins.triodosbe:TriodosBePlugin']
          },
      install_requires=['ofxstatement'],
      include_package_data=True,
      zip_safe=True
      )

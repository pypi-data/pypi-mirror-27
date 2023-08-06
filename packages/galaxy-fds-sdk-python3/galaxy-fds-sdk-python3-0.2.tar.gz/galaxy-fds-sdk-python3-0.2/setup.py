# -*- coding: utf-8 -*-
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(
  name='galaxy-fds-sdk-python3',
  version='0.2',
  author='http://xiangyang.li',
  author_email='shawn@xiangyang.li',
  include_package_data=True,
  install_requires=['requests>=2.6.0', 'argcomplete>=1.4.1'],
  license='Apache License',
  packages=['fds', 'fds.auth', 'fds.auth.signature', 'fds.model'],
  description='Galaxy FDS SDK for Python3.x',
  entry_points={
    'console_scripts': [
      'fds=fds.fds_cmd:main'
    ]
  }
)

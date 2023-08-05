#!/usr/bin/env python

from distutils.core import setup

setup(name='descpipe',
      version='1.3',
      scripts=['bin/descpipe'],
      packages=['descpipe', 'descpipe.launcher'],
      install_requires=['pyyaml','py-dag']
      )

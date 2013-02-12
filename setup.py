#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

def get_version():
    f = open('gitlab.py')
    try:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])
    finally:
        f.close()

setup(name='python-gitlab',
      version=get_version(),
      description='Interact with GitLab API',
      long_description='Interact with GitLab API',
      author='Gauvain Pocentek',
      author_email='gauvain@pocentek.net',
      license='LGPLv3',
      url='https://github.com/gpocentek/python-gitlab',
      py_modules=['gitlab'],
      )

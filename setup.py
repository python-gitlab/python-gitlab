#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

import gitlab


def get_version():

    return gitlab.__version__


setup(name='python-gitlab',
      version=get_version(),
      description='Interact with GitLab API',
      long_description='Interact with GitLab API',
      author='Gauvain Pocentek',
      author_email='gauvain@pocentek.net',
      license='LGPLv3',
      url='https://github.com/gpocentek/python-gitlab',
      packages=['gitlab'],
      scripts=['bin/gitlab'],
      install_requires=['requests', 'six'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows'
        ]
      )

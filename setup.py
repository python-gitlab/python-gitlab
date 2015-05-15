#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

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
      packages=find_packages(),
      install_requires=['requests', 'six'],
      entry_points={
          'console_scripts': [
              'gitlab = gitlab.cli:main'
          ]
      },
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

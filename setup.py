#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


def get_version():
    with open('gitlab/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(name='python-gitlab',
      version=get_version(),
      description='Interact with GitLab API',
      long_description='Interact with GitLab API',
      author='Gauvain Pocentek',
      author_email='gauvain@pocentek.net',
      license='LGPLv3',
      url='https://github.com/python-gitlab/python-gitlab',
      packages=find_packages(),
      install_requires=['requests>=1.0', 'six'],
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

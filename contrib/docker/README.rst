python-gitlab docker image
==========================

Dockerfile contributed by *oupala*:
https://github.com/python-gitlab/python-gitlab/issues/295

How to build
------------

``docker build -t me/python-gitlab:VERSION .``

How to use
----------

``docker run -it -v /path/to/python-gitlab.cfg:/python-gitlab.cfg python-gitlab <command> ...``

To make things easier you can create a shell alias:

``alias gitlab='docker run --rm -it -v /path/to/python-gitlab.cfg:/python-gitlab.cfg python-gitlab``

python-gitlab docker image
==========================

How to build
------------

``docker build -t python-gitlab:VERSION .``

How to use
----------

``docker run -it --rm  -e GITLAB_PRIVATE_TOKEN=<your token> =/python-gitlab.cfg python-gitlab <command> ...``

To change the endpoint, add `-e GITLAB_URL=<your url>`


Bring your own config file:
``docker run -it --rm -v /path/to/python-gitlab.cfg:/python-gitlab.cfg -e GITLAB_CFG=/python-gitlab.cfg python-gitlab <command> ...``



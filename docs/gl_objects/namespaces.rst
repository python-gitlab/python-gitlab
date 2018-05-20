##########
Namespaces
##########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Namespace`
  + :class:`gitlab.v4.objects.NamespaceManager`
  + :attr:`gitlab.Gitlab.namespaces`

* GitLab API: https://docs.gitlab.com/ce/api/namespaces.html

Examples
--------

List namespaces::

    namespaces = gl.namespaces.list()

Search namespaces::

    namespaces = gl.namespaces.list(search='foo')

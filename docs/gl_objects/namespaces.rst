##########
Namespaces
##########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Namespace`
  + :class:`gitlab.v4.objects.NamespaceManager`
  + :attr:`gitlab.Gitlab.namespaces`

* v3 API:

  + :class:`gitlab.v3.objects.Namespace`
  + :class:`gitlab.v3.objects.NamespaceManager`
  + :attr:`gitlab.Gitlab.namespaces`

* GitLab API: https://docs.gitlab.com/ce/api/namespaces.html

Examples
--------

List namespaces:

.. literalinclude:: namespaces.py
   :start-after: # list
   :end-before: # end list

Search namespaces:

.. literalinclude:: namespaces.py
   :start-after: # search
   :end-before: # end search

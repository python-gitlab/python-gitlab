###########
Deploy keys
###########

Deploy keys
===========

Use :class:`~gitlab.objects.Key` objects to manipulate deploy keys. The
:attr:`gitlab.Gitlab.keys` manager object provides helper functions.

Examples
--------

List the deploy keys:

.. literalinclude:: deploy_keys.py
   :start-after: # global list
   :end-before: # end global list

Get a single deploy key:

.. literalinclude:: deploy_keys.py
   :start-after: # global get
   :end-before: # end global get

Deploy keys for projects
========================

Use :class:`~gitlab.objects.ProjectKey` objects to manipulate deploy keys for
projects. The :attr:`gitlab.Gitlab.project_keys` and :attr:`Project.keys
<gitlab.objects.Project.keys>` manager objects provide helper functions.

Examples
--------

List keys for a project:

.. literalinclude:: deploy_keys.py
   :start-after: # list
   :end-before: # end list

Get a single deploy key:

.. literalinclude:: deploy_keys.py
   :start-after: # get
   :end-before: # end get

Create a deploy key for a project:

.. literalinclude:: deploy_keys.py
   :start-after: # create
   :end-before: # end create

Delete a deploy key for a project:

.. literalinclude:: deploy_keys.py
   :start-after: # delete
   :end-before: # end delete

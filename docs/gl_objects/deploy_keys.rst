###########
Deploy keys
###########

Deploy keys
===========

Deploy keys allow read-only access to multiple projects with a single SSH key.

* Object class: :class:`~gitlab.objects.DeployKey`
* Manager object: :attr:`gitlab.Gitlab.deploykeys`

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

Deploy keys can be managed on a per-project basis.

* Object class: :class:`~gitlab.objects.ProjectKey`
* Manager objects: :attr:`gitlab.Gitlab.project_keys` and :attr:`Project.keys
  <gitlab.objects.Project.keys>`

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

Enable a deploy key for a project:

.. literalinclude:: deploy_keys.py
   :start-after: # enable
   :end-before: # end enable

Disable a deploy key for a project:

.. literalinclude:: deploy_keys.py
   :start-after: # disable
   :end-before: # end disable

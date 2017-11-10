###########
Deploy keys
###########

Deploy keys
===========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.DeployKey`
  + :class:`gitlab.v4.objects.DeployKeyManager`
  + :attr:`gitlab.Gitlab.deploykeys`

* v3 API:

  + :class:`gitlab.v3.objects.DeployKey`
  + :class:`gitlab.v3.objects.DeployKeyManager`
  + :attr:`gitlab.Gitlab.deploykeys`

* GitLab API: https://docs.gitlab.com/ce/api/deploy_keys.html

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

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectKey`
  + :class:`gitlab.v4.objects.ProjectKeyManager`
  + :attr:`gitlab.v4.objects.Project.keys`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectKey`
  + :class:`gitlab.v3.objects.ProjectKeyManager`
  + :attr:`gitlab.v3.objects.Project.keys`
  + :attr:`gitlab.Gitlab.project_keys`

* GitLab API: https://docs.gitlab.com/ce/api/deploy_keys.html

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

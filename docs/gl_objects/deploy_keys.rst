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

* GitLab API: https://docs.gitlab.com/ce/api/deploy_keys.html

Examples
--------

List the deploy keys::

    keys = gl.deploykeys.list()

Deploy keys for projects
========================

Deploy keys can be managed on a per-project basis.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectKey`
  + :class:`gitlab.v4.objects.ProjectKeyManager`
  + :attr:`gitlab.v4.objects.Project.keys`

* GitLab API: https://docs.gitlab.com/ce/api/deploy_keys.html

Examples
--------

List keys for a project::

    keys = project.keys.list()

Get a single deploy key::

    key = project.keys.get(key_id)

Create a deploy key for a project::

    key = project.keys.create({'title': 'jenkins key',
                               'key': open('/home/me/.ssh/id_rsa.pub').read()})

Delete a deploy key for a project::

    key = project.keys.list(key_id)
    # or
    key.delete()

Enable a deploy key for a project::

    project.keys.enable(key_id)

Disable a deploy key for a project::

    project.keys.delete(key_id)

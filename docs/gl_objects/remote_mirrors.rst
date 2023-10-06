######################
Project Remote Mirrors
######################

Remote Mirrors allow you to set up push mirroring for a project.

References
==========

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRemoteMirror`
  + :class:`gitlab.v4.objects.ProjectRemoteMirrorManager`
  + :attr:`gitlab.v4.objects.Project.remote_mirrors`

* GitLab API: https://docs.gitlab.com/ce/api/remote_mirrors.html

Examples
--------

Get the list of a project's remote mirrors::

    mirrors = project.remote_mirrors.list()

Create (and enable) a remote mirror for a project::

    mirror = project.remote_mirrors.create({'url': 'https://gitlab.com/example.git',
                                            'enabled': True})

Update an existing remote mirror's attributes::

    mirror.enabled = False
    mirror.only_protected_branches = True
    mirror.save()

Delete an existing remote mirror::

  mirror.delete()

######################
Project Pull Mirror
######################

Pull Mirror allow you to set up pull mirroring for a project.

References
==========

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPullMirror`
  + :class:`gitlab.v4.objects.ProjectPullMirrorManager`
  + :attr:`gitlab.v4.objects.Project.pull_mirror`

* GitLab API: https://docs.gitlab.com/api/project_pull_mirroring/

Examples
--------

Get the current pull mirror of a project::

    mirrors = project.pull_mirror.get()

Create (and enable) a remote mirror for a project::

    mirror = project.pull_mirror.create({'url': 'https://gitlab.com/example.git',
                                            'enabled': True})

Update an existing remote mirror's attributes::

    mirror.enabled = False
    mirror.only_protected_branches = True
    mirror.save()

Start a sync of the pull mirror::

  project.pull_mirror.start()

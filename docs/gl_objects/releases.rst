########
Releases
########

Project releases
================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRelease`
  + :class:`gitlab.v4.objects.ProjectReleaseManager`
  + :attr:`gitlab.v4.objects.Project.releases`

* Gitlab API: https://docs.gitlab.com/ee/api/releases/index.html

Examples
--------

Get a list of releases from a project::

    project = gl.projects.get(project_id, lazy=True)
    release = project.releases.list()

Get a single release::

    release = project.releases.get('v1.2.3')

Edit a release::

    release.name = "Demo Release"
    release.description = "release notes go here"
    release.save()

Create a release for a project tag::

    release = project.releases.create({'name':'Demo Release', 'tag_name':'v1.2.3', 'description':'release notes go here'})

Delete a release::

    # via its tag name from project attributes
    release = project.releases.delete('v1.2.3')

    # delete object directly
    release.delete()

.. note::

    The Releases API is one of the few working with ``CI_JOB_TOKEN``, but the project can't
    be fetched with the token. Thus use `lazy` for the project as in the above example.

    Also be aware that most of the capabilities of the endpoint were not accessible with
    ``CI_JOB_TOKEN`` until Gitlab version 14.5.

Project release links
=====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectReleaseLink`
  + :class:`gitlab.v4.objects.ProjectReleaseLinkManager`
  + :attr:`gitlab.v4.objects.ProjectRelease.links`

* Gitlab API: https://docs.gitlab.com/ee/api/releases/links.html

Examples
--------

Get a list of releases from a project::

    links = release.links.list()

Get a single release link::

    link = release.links.get(1)

Create a release link for a release::

    link = release.links.create({"url": "https://example.com/asset", "name": "asset"})

Delete a release link::

    # via its ID from release attributes
    release.links.delete(1)

    # delete object directly
    link.delete()

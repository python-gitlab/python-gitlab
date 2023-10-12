########
Packages
########

Packages allow you to utilize GitLab as a private repository for a variety
of common package managers, as well as GitLab's generic package registry.

Project Packages
=====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPackage`
  + :class:`gitlab.v4.objects.ProjectPackageManager`
  + :attr:`gitlab.v4.objects.Project.packages`

* GitLab API: https://docs.gitlab.com/ee/api/packages.html#within-a-project

Examples
--------

List the packages in a project::

    packages = project.packages.list()

Filter the results by ``package_type`` or ``package_name`` ::

    packages = project.packages.list(package_type='pypi')

Get a specific package of a project by id::

    package = project.packages.get(1)

Delete a package from a project::

    package.delete()
    # or
    project.packages.delete(package.id)


Group Packages
===================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupPackage`
  + :class:`gitlab.v4.objects.GroupPackageManager`
  + :attr:`gitlab.v4.objects.Group.packages`

* GitLab API: https://docs.gitlab.com/ee/api/packages.html#within-a-group

Examples
--------

List the packages in a group::

    packages = group.packages.list()

Filter the results by ``package_type`` or ``package_name`` ::

    packages = group.packages.list(package_type='pypi')


Project Package Files
=====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPackageFile`
  + :class:`gitlab.v4.objects.ProjectPackageFileManager`
  + :attr:`gitlab.v4.objects.ProjectPackage.package_files`

* GitLab API: https://docs.gitlab.com/ee/api/packages.html#list-package-files

Examples
--------

List package files for package in project::

    package = project.packages.get(1)
    package_files = package.package_files.list()

Delete a package file in a project::

    package = project.packages.get(1)
    file = package.package_files.list()[0]
    file.delete()

Project Package Pipelines
=========================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPackagePipeline`
  + :class:`gitlab.v4.objects.ProjectPackagePipelineManager`
  + :attr:`gitlab.v4.objects.ProjectPackage.pipelines`

* GitLab API: https://docs.gitlab.com/ee/api/packages.html#list-package-pipelines

Examples
--------

List package pipelines for package in project::

    package = project.packages.get(1)
    package_pipelines = package.pipelines.list()

Generic Packages
================

You can use python-gitlab to upload and download generic packages.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GenericPackage`
  + :class:`gitlab.v4.objects.GenericPackageManager`
  + :attr:`gitlab.v4.objects.Project.generic_packages`

* GitLab API: https://docs.gitlab.com/ee/user/packages/generic_packages

Examples
--------

Upload a generic package to a project::

    project = gl.projects.get(1, lazy=True)
    package = project.generic_packages.upload(
        package_name="hello-world",
        package_version="v1.0.0",
        file_name="hello.tar.gz",
        path="/path/to/local/hello.tar.gz"
    )

Download a project's generic package::

    project = gl.projects.get(1, lazy=True)
    package = project.generic_packages.download(
        package_name="hello-world",
        package_version="v1.0.0",
        file_name="hello.tar.gz",
    )

.. hint:: You can use the Packages API described above to find packages and
    retrieve the metadata you need download them.

#######
Packages
#######

Packages allow you to utilize GitLab as a private repository for a variety
of common package managers.

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

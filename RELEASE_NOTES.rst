#############
Release notes
#############

This page describes important changes between python-gitlab releases.

Changes from 0.19 to 0.20
=========================

* The ``projects`` attribute of ``Group`` objects is not a list of ``Project``
  objects anymore. It is a Manager object giving access to ``GroupProject``
  objects. To get the list of projects use:

  .. code-block:: python

     group.projects.list()

  Documentation:
  http://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html#examples

  Related issue: https://github.com/python-gitlab/python-gitlab/issues/209

* The ``Key`` objects are deprecated in favor of the new ``DeployKey`` objects.
  They are exactly the same but the name makes more sense.

  Documentation:
  http://python-gitlab.readthedocs.io/en/stable/gl_objects/deploy_keys.html

  Related issue: https://github.com/python-gitlab/python-gitlab/issues/212

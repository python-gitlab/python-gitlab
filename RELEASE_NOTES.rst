###############################
Release notes for python-gitlab
###############################

This page describes important changes between python-gitlab releases.

Changes from 0.19 to 0.20
=========================

* The ``projects`` attribute of ``Group`` objects is not a list of ``Project``
  objects anymore. It is a Manager object giving access to ``GroupProject``
  objects. To get the list of projects use:

  .. code-block:: python

     group.projects.list()

  Documentation for ``Group`` objects:
  http://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html#examples

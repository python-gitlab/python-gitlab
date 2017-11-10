#############
Release notes
#############

This page describes important changes between python-gitlab releases.

Changes from 1.1 to 1.2
=======================

* The following deprecated methods and objects have been removed:

  * gitlab.v3.object ``Key`` and ``KeyManager`` objects: use ``DeployKey`` and
    ``DeployKeyManager`` instead
  * gitlab.v3.objects.Project ``archive_`` and ``unarchive_`` methods
  * gitlab.Gitlab ``credentials_auth``, ``token_auth``, ``set_url``,
    ``set_token`` and ``set_credentials`` methods. Once a Gitlab object has been
    created its URL and authentication information cannot be updated: create a
    new Gitlab object if you need to use new information

Changes from 1.0.2 to 1.1
=========================

* The ``ProjectUser`` class doesn't inherit from ``User`` anymore, and the
  ``GroupProject`` class doesn't inherit from ``Project`` anymore. The Gitlab
  API doesn't provide the same set of features for these objects, so
  python-gitlab objects shouldn't try to workaround that.

  You can create ``User`` or ``Project`` objects from ``ProjectUser`` and
  ``GroupProject`` objects using the ``id`` attribute:

  .. code-block:: python

     for gr_project in group.projects.list():
         # lazy object creation avoids a Gitlab API request
         project = gl.projects.get(gr_project.id, lazy=True)
         project.default_branch = 'develop'
         project.save()

Changes from 0.21 to 1.0.0
==========================

1.0.0 brings a stable python-gitlab API for the v4 Gitlab API. v3 is still used
by default.

v4 is mostly compatible with the v3, but some important changes have been
introduced. Make sure to read `Switching to GtiLab API v4
<http://python-gitlab.readthedocs.io/en/master/switching-to-v4.html>`_.

The development focus will be v4 from now on. v3 has been deprecated by GitLab
and will disappear from python-gitlab at some point.

Changes from 0.20 to 0.21
=========================

* Initial support for the v4 API (experimental)

  The support for v4 is stable enough to be tested, but some features might be
  broken. Please report issues to
  https://github.com/python-gitlab/python-gitlab/issues/

  Be aware that the python-gitlab API for v4 objects might change in the next
  releases.

  .. warning::

     Consider defining explicitly which API version you want to use in the
     configuration files or in your ``gitlab.Gitlab`` instances. The default
     will change from v3 to v4 soon.

* Several methods have been deprecated in the ``gitlab.Gitlab`` class:

  + ``credentials_auth()`` is deprecated and will be removed. Call ``auth()``.
  + ``token_auth()`` is deprecated and will be removed. Call ``auth()``.
  + ``set_url()`` is deprecated, create a new ``Gitlab`` instance if you need
    an updated URL.
  + ``set_token()`` is deprecated, use the ``private_token`` argument of the
    ``Gitlab`` constructor.
  + ``set_credentials()`` is deprecated, use the ``email`` and ``password``
    arguments of the ``Gitlab`` constructor.

* The service listing method (``ProjectServiceManager.list()``) now returns a
  python list instead of a JSON string.

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

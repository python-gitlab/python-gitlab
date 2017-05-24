#############
Release notes
#############

This page describes important changes between python-gitlab releases.

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

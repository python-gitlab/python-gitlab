#############
Release notes
#############

Prior to version 2.0.0 and GitHub Releases, a summary of changes was maintained
in release notes. They are available below for historical purposes.
For the list of current releases, including breaking changes, please see the changelog.

Changes from 1.8 to 1.9
=======================

* ``ProjectMemberManager.all()`` and ``GroupMemberManager.all()`` now return a
  list of ``ProjectMember`` and ``GroupMember`` objects respectively, instead
  of a list of dicts.

Changes from 1.7 to 1.8
=======================

* You can now use the ``query_parameters`` argument in method calls to define
  arguments to send to the GitLab server. This allows to avoid conflicts
  between python-gitlab and GitLab server variables, and allows to use the
  python reserved keywords as GitLab arguments.

  The following examples make the same GitLab request with the 2 syntaxes::

     projects = gl.projects.list(owned=True, starred=True)
     projects = gl.projects.list(query_parameters={'owned': True, 'starred': True})

  The following example only works with the new parameter::

     activities = gl.user_activities.list(
                    query_parameters={'from': '2019-01-01'},
                    all=True)

* Additionally the ``all`` paremeter is not sent to the GitLab anymore.

Changes from 1.5 to 1.6
=======================

* When python-gitlab detects HTTP redirections from http to https it will raise
  a RedirectionError instead of a cryptic error.

  Make sure to use an ``https://`` protocol in your GitLab URL parameter if the
  server requires it.

Changes from 1.4 to 1.5
=======================

* APIv3 support has been removed. Use the 1.4 release/branch if you need v3
  support.
* GitLab EE features are now supported: Geo nodes, issue links, LDAP groups,
  project/group boards, project mirror pulling, project push rules, EE license
  configuration, epics.
* The ``GetFromListMixin`` class has been removed. The ``get()`` method is not
  available anymore for the following managers:

  - UserKeyManager
  - DeployKeyManager
  - GroupAccessRequestManager
  - GroupIssueManager
  - GroupProjectManager
  - GroupSubgroupManager
  - IssueManager
  - ProjectCommitStatusManager
  - ProjectEnvironmentManager
  - ProjectLabelManager
  - ProjectPipelineJobManager
  - ProjectAccessRequestManager
  - TodoManager

* ``ProjectPipelineJob`` do not heritate from ``ProjectJob`` anymore and thus
  can only be listed.

Changes from 1.3 to 1.4
=======================

* 1.4 is the last release supporting the v3 API, and the related code will be
  removed in the 1.5 version.

  If you are using a Gitlab server version that does not support the v4 API you
  can:

  * upgrade the server (recommended)
  * make sure to use version 1.4 of python-gitlab (``pip install
    python-gitlab==1.4``)

  See also the `Switching to GitLab API v4 documentation
  <http://python-gitlab.readthedocs.io/en/master/switching-to-v4.html>`__.
* python-gitlab now handles the server rate limiting feature. It will pause for
  the required time when reaching the limit (`documentation
  <http://python-gitlab.readthedocs.io/en/master/api-usage.html#rate-limits>`__)
* The ``GetFromListMixin.get()`` method is deprecated and will be removed in
  the next python-gitlab version. The goal of this mixin/method is to provide a
  way to get an object by looping through a list for GitLab objects that don't
  support the GET method. The method `is broken
  <https://github.com/python-gitlab/python-gitlab/issues/499>`__ and conflicts
  with the GET method now supported by some GitLab objects.

  You can implement your own method with something like:

  .. code-block:: python

     def get_from_list(self, id):
         for obj in self.list(as_list=False):
             if obj.get_id() == id:
                 return obj

* The ``GroupMemberManager``, ``NamespaceManager`` and ``ProjectBoardManager``
  managers now use the GET API from GitLab instead of the
  ``GetFromListMixin.get()`` method.


Changes from 1.2 to 1.3
=======================

* ``gitlab.Gitlab`` objects can be used as context managers in a ``with``
  block.

Changes from 1.1 to 1.2
=======================

* python-gitlab now respects the ``*_proxy``, ``REQUESTS_CA_BUNDLE`` and
  ``CURL_CA_BUNDLE`` environment variables (#352)
* The following deprecated methods and objects have been removed:

  * gitlab.v3.object ``Key`` and ``KeyManager`` objects: use ``DeployKey`` and
    ``DeployKeyManager`` instead
  * gitlab.v3.objects.Project ``archive_`` and ``unarchive_`` methods
  * gitlab.Gitlab ``credentials_auth``, ``token_auth``, ``set_url``,
    ``set_token`` and ``set_credentials`` methods. Once a Gitlab object has been
    created its URL and authentication information cannot be updated: create a
    new Gitlab object if you need to use new information
* The ``todo()`` method raises a ``GitlabTodoError`` exception on error

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
introduced. Make sure to read `Switching to GitLab API v4
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

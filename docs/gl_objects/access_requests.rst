###############
Access requests
###############

Users can request access to groups and projects.

When access is granted the user should be given a numerical access level. The
following constants are provided to represent the access levels:

* ``gitlab.const.AccessLevel.GUEST``: ``10``
* ``gitlab.const.AccessLevel.REPORTER``: ``20``
* ``gitlab.const.AccessLevel.DEVELOPER``: ``30``
* ``gitlab.const.AccessLevel.MAINTAINER``: ``40``
* ``gitlab.const.AccessLevel.OWNER``: ``50``

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectAccessRequest`
  + :class:`gitlab.v4.objects.ProjectAccessRequestManager`
  + :attr:`gitlab.v4.objects.Project.accessrequests`
  + :class:`gitlab.v4.objects.GroupAccessRequest`
  + :class:`gitlab.v4.objects.GroupAccessRequestManager`
  + :attr:`gitlab.v4.objects.Group.accessrequests`

* GitLab API: https://docs.gitlab.com/ce/api/access_requests.html

Examples
--------

List access requests from projects and groups::

    p_ars = project.accessrequests.list()
    g_ars = group.accessrequests.list()

Create an access request::

    p_ar = project.accessrequests.create()
    g_ar = group.accessrequests.create()

Approve an access request::

    ar.approve()  # defaults to DEVELOPER level
    ar.approve(access_level=gitlab.const.AccessLevel.MAINTAINER)  # explicitly set access level

Deny (delete) an access request::

    project.accessrequests.delete(user_id)
    group.accessrequests.delete(user_id)
    # or
    ar.delete()

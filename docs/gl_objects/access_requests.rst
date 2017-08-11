###############
Access requests
###############

Users can request access to groups and projects.

When access is granted the user should be given a numerical access level. The
following constants are provided to represent the access levels:

* ``gitlab.GUEST_ACCESS``: ``10``
* ``gitlab.REPORTER_ACCESS``: ``20``
* ``gitlab.DEVELOPER_ACCESS``: ``30``
* ``gitlab.MASTER_ACCESS``: ``40``
* ``gitlab.OWNER_ACCESS``: ``50``

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectAccessRequest`
  + :class:`gitlab.v4.objects.ProjectAccessRequestManager`
  + :attr:`gitlab.v4.objects.Project.accessrequests`
  + :class:`gitlab.v4.objects.GroupAccessRequest`
  + :class:`gitlab.v4.objects.GroupAccessRequestManager`
  + :attr:`gitlab.v4.objects.Group.accessrequests`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectAccessRequest`
  + :class:`gitlab.v3.objects.ProjectAccessRequestManager`
  + :attr:`gitlab.v3.objects.Project.accessrequests`
  + :attr:`gitlab.Gitlab.project_accessrequests`
  + :class:`gitlab.v3.objects.GroupAccessRequest`
  + :class:`gitlab.v3.objects.GroupAccessRequestManager`
  + :attr:`gitlab.v3.objects.Group.accessrequests`
  + :attr:`gitlab.Gitlab.group_accessrequests`

* GitLab API: https://docs.gitlab.com/ce/api/access_requests.html

Examples
--------

List access requests from projects and groups:

.. literalinclude:: access_requests.py
   :start-after: # list
   :end-before: # end list

Get a single request:

.. literalinclude:: access_requests.py
   :start-after: # get
   :end-before: # end get

Create an access request:

.. literalinclude:: access_requests.py
   :start-after: # create
   :end-before: # end create

Approve an access request:

.. literalinclude:: access_requests.py
   :start-after: # approve
   :end-before: # end approve

Deny (delete) an access request:

.. literalinclude:: access_requests.py
   :start-after: # delete
   :end-before: # end delete

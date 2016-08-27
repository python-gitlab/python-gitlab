###############
Access requests
###############

Use :class:`~gitlab.objects.ProjectAccessRequest` and
:class:`~gitlab.objects.GroupAccessRequest` objects to manipulate access
requests for projects and groups. The
:attr:`gitlab.Gitlab.project_accessrequests`,
:attr:`gitlab.Gitlab.group_accessrequests`, :attr:`Project.accessrequests
<gitlab.objects.Project.accessrequests>` and :attr:`Group.accessrequests
<gitlab.objects.Group.accessrequests>` manager objects provide helper
functions.

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

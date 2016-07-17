######
Groups
######

Groups
======

Use :class:`~gitlab.objects.Group` objects to manipulate groups. The
:attr:`gitlab.Gitlab.groups` manager object provides helper functions.

Examples
--------

List the groups:

.. literalinclude:: groups.py
   :start-after: # list
   :end-before: # end list

Search groups:

.. literalinclude:: groups.py
   :start-after: # search
   :end-before: # end search

Get a group's detail:

.. literalinclude:: groups.py
   :start-after: # get
   :end-before: # end get

List a group's projects:

.. literalinclude:: groups.py
   :start-after: # projects list
   :end-before: # end projects list

You can filter and sort the result using the following parameters:

* ``archived``: limit by archived status
* ``visibility``: limit by visibility. Allowed values are ``public``,
  ``internal`` and ``private``
* ``search``: limit to groups matching the given value
* ``order_by``: sort by criteria. Allowed values are ``id``, ``name``, ``path``,
  ``created_at``, ``updated_at`` and ``last_activity_at``
* ``sort``: sort order: ``asc`` or ``desc``
* ``ci_enabled_first``: return CI enabled groups first

Create a group:

.. literalinclude:: groups.py
   :start-after: # create
   :end-before: # end create

Update a group:

.. literalinclude:: groups.py
   :start-after: # update
   :end-before: # end update

Remove a group:

.. literalinclude:: groups.py
   :start-after: # delete
   :end-before: # end delete

Group members
=============

Use :class:`~gitlab.objects.GroupMember` objects to manipulate groups. The
:attr:`gitlab.Gitlab.group_members` and :attr:`Group.members
<gitlab.objects.Group.members>` manager objects provide helper functions.

The following :class:`~gitlab.objects.Group` attributes define the supported
access levels:

* ``GUEST_ACCESS = 10``
* ``REPORTER_ACCESS = 20``
* ``DEVELOPER_ACCESS = 30``
* ``MASTER_ACCESS = 40``
* ``OWNER_ACCESS = 50``

List group members:

.. literalinclude:: groups.py
   :start-after: # member list
   :end-before: # end member list

Get a group member:

.. literalinclude:: groups.py
   :start-after: # member get
   :end-before: # end member get

Add a member to the group:

.. literalinclude:: groups.py
   :start-after: # member create
   :end-before: # end member create

Update a member (change the access level):

.. literalinclude:: groups.py
   :start-after: # member update
   :end-before: # end member update

Remove a member from the group:

.. literalinclude:: groups.py
   :start-after: # member delete
   :end-before: # end member delete

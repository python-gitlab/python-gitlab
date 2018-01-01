######
Groups
######

Groups
======

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Group`
  + :class:`gitlab.v4.objects.GroupManager`
  + :attr:`gitlab.Gitlab.groups`

* v3 API:

  + :class:`gitlab.v3.objects.Group`
  + :class:`gitlab.v3.objects.GroupManager`
  + :attr:`gitlab.Gitlab.groups`

* GitLab API: https://docs.gitlab.com/ce/api/groups.html

Examples
--------

List the groups:

.. literalinclude:: groups.py
   :start-after: # list
   :end-before: # end list

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

Subgroups
=========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupSubgroup`
  + :class:`gitlab.v4.objects.GroupSubgroupManager`
  + :attr:`gitlab.v4.objects.Group.subgroups`

Examples
--------

List the subgroups for a group::

    subgroups = group.subgroups.list()

Group custom attributes
=======================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupCustomAttribute`
  + :class:`gitlab.v4.objects.GroupCustomAttributeManager`
  + :attr:`gitlab.v4.objects.Group.customattributes`

* GitLab API: https://docs.gitlab.com/ce/api/custom_attributes.html

Examples
--------

List custom attributes for a group::

    attrs = group.customattributes.list()

Get a custom attribute for a group::

    attr = group.customattributes.get(attr_key)

Set (create or update) a custom attribute for a group::

    attr = group.customattributes.set(attr_key, attr_value)

Delete a custom attribute for a group::

    attr.delete()
    # or
    group.customattributes.delete(attr_key)

Group members
=============

The following constants define the supported access levels:

* ``gitlab.GUEST_ACCESS = 10``
* ``gitlab.REPORTER_ACCESS = 20``
* ``gitlab.DEVELOPER_ACCESS = 30``
* ``gitlab.MASTER_ACCESS = 40``
* ``gitlab.OWNER_ACCESS = 50``

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupMember`
  + :class:`gitlab.v4.objects.GroupMemberManager`
  + :attr:`gitlab.v4.objects.Group.members`

* v3 API:

  + :class:`gitlab.v3.objects.GroupMember`
  + :class:`gitlab.v3.objects.GroupMemberManager`
  + :attr:`gitlab.v3.objects.Group.members`
  + :attr:`gitlab.Gitlab.group_members`

* GitLab API: https://docs.gitlab.com/ce/api/groups.html


Examples
--------

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

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

* GitLab API: https://docs.gitlab.com/ce/api/groups.html

Examples
--------

List the groups::

    groups = gl.groups.list()

Get a group's detail::

    group = gl.groups.get(group_id)

List a group's projects::

    projects = group.projects.list()

You can filter and sort the result using the following parameters:

* ``archived``: limit by archived status
* ``visibility``: limit by visibility. Allowed values are ``public``,
  ``internal`` and ``private``
* ``search``: limit to groups matching the given value
* ``order_by``: sort by criteria. Allowed values are ``id``, ``name``, ``path``,
  ``created_at``, ``updated_at`` and ``last_activity_at``
* ``sort``: sort order: ``asc`` or ``desc``
* ``ci_enabled_first``: return CI enabled groups first

Create a group::

    group = gl.groups.create({'name': 'group1', 'path': 'group1'})

Update a group::

    group.description = 'My awesome group'
    group.save()

Remove a group::

    gl.group.delete(group_id)
    # or
    group.delete()

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

    # The GroupSubgroup objects don't expose the same API as the Group
    # objects. If you need to manipulate a subgroup as a group, create a new
    # Group object:
    real_group = gl.groups.get(subgroup_id, lazy=True)
    real_group.issues.list()

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

Search groups by custom attribute::

    group.customattributes.set('role': 'admin')
    gl.groups.list(custom_attributes={'role': 'admin'})

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

* GitLab API: https://docs.gitlab.com/ce/api/groups.html


Examples
--------

List group members::

    members = group.members.list()

Get a group member::

    members = group.members.get(member_id)

Add a member to the group::

    member = group.members.create({'user_id': user_id,
                                   'access_level': gitlab.GUEST_ACCESS})

Update a member (change the access level)::

    member.access_level = gitlab.DEVELOPER_ACCESS
    member.save()

Remove a member from the group::

    group.members.delete(member_id)
    # or
    member.delete()

LDAP group links
================

Add an LDAP group link to an existing GitLab group::

    group.add_ldap_group_link(ldap_group_cn, gitlab.DEVELOPER_ACCESS, 'main')

Remove a link::

    group.delete_ldap_group_link(ldap_group_cn, 'main')

Sync the LDAP groups::

    group.ldap_sync()

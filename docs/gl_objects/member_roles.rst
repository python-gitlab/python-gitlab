############
Member Roles
############

You can configure member roles at the instance-level (admin only), or 
at group level.

Instance-level member roles
===========================

This endpoint requires admin access.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.MemberRole`
  + :class:`gitlab.v4.objects.MemberRoleManager`
  + :attr:`gitlab.Gitlab.member_roles`

* GitLab API

  + https://docs.gitlab.com/api/member_roles#manage-instance-member-roles

Examples
--------

List member roles::

    variables = gl.member_roles.list()

Create a member role::

    variable = gl.member_roles.create({'name': 'Custom Role', 'base_access_level': value})

Remove a member role::

    gl.member_roles.delete(member_role_id)

Group member role
=================

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.GroupMemberRole`
  + :class:`gitlab.v4.objects.GroupMemberRoleManager`
  + :attr:`gitlab.v4.objects.Group.member_roles`

* GitLab API

  + https://docs.gitlab.com/api/member_roles#manage-group-member-roles

Examples
--------

List member roles::

    member_roles = group.member_roles.list()

Create a member role::

    member_roles = group.member_roles.create({'name': 'Custom Role', 'base_access_level': value})

Remove a member role::

    gl.member_roles.delete(member_role_id)


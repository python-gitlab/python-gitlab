.. _users_examples:

######################
Users and current user
######################

The Gitlab API exposes user-related method that can be manipulated by admins
only.

The currently logged-in user is also exposed.

Users
=====

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.User`
  + :class:`gitlab.v4.objects.UserManager`
  + :attr:`gitlab.Gitlab.users`

* GitLab API:

  + https://docs.gitlab.com/ce/api/users.html
  + https://docs.gitlab.com/ee/api/projects.html#list-projects-starred-by-a-user

Examples
--------

Get the list of users::

    users = gl.users.list()

Search users whose username match a given string::

    users = gl.users.list(search='foo')

Get a single user::

    # by ID
    user = gl.users.get(user_id)
    # by username
    user = gl.users.list(username='root')[0]

Create a user::

    user = gl.users.create({'email': 'john@doe.com',
                            'password': 's3cur3s3cr3T',
                            'username': 'jdoe',
                            'name': 'John Doe'})

Update a user::

    user.name = 'Real Name'
    user.save()

Delete a user::

    gl.users.delete(user_id)
    # or
    user.delete()

Block/Unblock a user::

    user.block()
    user.unblock()

Activate/Deactivate a user::

    user.activate()
    user.deactivate()

Follow/Unfollow a user::

    user.follow()
    user.unfollow()

Set the avatar image for a user::

    # the avatar image can be passed as data (content of the file) or as a file
    # object opened in binary mode
    user.avatar = open('path/to/file.png', 'rb')
    user.save()

Set an external identity for a user::

    user.provider = 'oauth2_generic'
    user.extern_uid = '3'
    user.save()

Delete an external identity by provider name::

    user.identityproviders.delete('oauth2_generic')

Get the followers of a user

    user.followers_users.list()

Get the followings of a user

    user.following_users.list()

List a user's starred projects

    user.starred_projects.list()

User custom attributes
======================

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.UserCustomAttribute`
  + :class:`gitlab.v4.objects.UserCustomAttributeManager`
  + :attr:`gitlab.v4.objects.User.customattributes`

* GitLab API: https://docs.gitlab.com/ce/api/custom_attributes.html

Examples
--------

List custom attributes for a user::

    attrs = user.customattributes.list()

Get a custom attribute for a user::

    attr = user.customattributes.get(attr_key)

Set (create or update) a custom attribute for a user::

    attr = user.customattributes.set(attr_key, attr_value)

Delete a custom attribute for a user::

    attr.delete()
    # or
    user.customattributes.delete(attr_key)

Search users by custom attribute::

    user.customattributes.set('role', 'QA')
    gl.users.list(custom_attributes={'role': 'QA'})

User impersonation tokens
=========================

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.UserImpersonationToken`
  + :class:`gitlab.v4.objects.UserImpersonationTokenManager`
  + :attr:`gitlab.v4.objects.User.impersonationtokens`

* GitLab API: https://docs.gitlab.com/ce/api/users.html#get-all-impersonation-tokens-of-a-user

List impersonation tokens for a user::

    i_t = user.impersonationtokens.list(state='active')
    i_t = user.impersonationtokens.list(state='inactive')

Get an impersonation token for a user::

    i_t = user.impersonationtokens.get(i_t_id)

Create and use an impersonation token for a user::

    i_t = user.impersonationtokens.create({'name': 'token1', 'scopes': ['api']})
    # use the token to create a new gitlab connection
    user_gl = gitlab.Gitlab(gitlab_url, private_token=i_t.token)

Revoke (delete) an impersonation token for a user::

    i_t.delete()


User memberships
=========================

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.UserMembership`
  + :class:`gitlab.v4.objects.UserMembershipManager`
  + :attr:`gitlab.v4.objects.User.memberships`

* GitLab API: https://docs.gitlab.com/ee/api/users.html#user-memberships-admin-only

List direct memberships for a user::

    memberships = user.memberships.list()

List only direct project memberships::

    memberships = user.memberships.list(type='Project')

List only direct group memberships::

    memberships = user.memberships.list(type='Namespace')

Current User
============

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUser`
  + :class:`gitlab.v4.objects.CurrentUserManager`
  + :attr:`gitlab.Gitlab.user`

* GitLab API: https://docs.gitlab.com/ce/api/users.html

Examples
--------

Get the current user::

    gl.auth()
    current_user = gl.user

GPG keys
========

References
----------

You can manipulate GPG keys for the current user and for the other users if you
are admin.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserGPGKey`
  + :class:`gitlab.v4.objects.CurrentUserGPGKeyManager`
  + :attr:`gitlab.v4.objects.CurrentUser.gpgkeys`
  + :class:`gitlab.v4.objects.UserGPGKey`
  + :class:`gitlab.v4.objects.UserGPGKeyManager`
  + :attr:`gitlab.v4.objects.User.gpgkeys`

* GitLab API: https://docs.gitlab.com/ce/api/users.html#list-all-gpg-keys

Examples
--------

List GPG keys for a user::

    gpgkeys = user.gpgkeys.list()

Get a GPG gpgkey for a user::

    gpgkey = user.gpgkeys.get(key_id)

Create a GPG gpgkey for a user::

    # get the key with `gpg --export -a GPG_KEY_ID`
    k = user.gpgkeys.create({'key': public_key_content})

Delete a GPG gpgkey for a user::

    user.gpgkeys.delete(key_id)
    # or
    gpgkey.delete()

SSH keys
========

References
----------

You can manipulate SSH keys for the current user and for the other users if you
are admin.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserKey`
  + :class:`gitlab.v4.objects.CurrentUserKeyManager`
  + :attr:`gitlab.v4.objects.CurrentUser.keys`
  + :class:`gitlab.v4.objects.UserKey`
  + :class:`gitlab.v4.objects.UserKeyManager`
  + :attr:`gitlab.v4.objects.User.keys`

* GitLab API: https://docs.gitlab.com/ce/api/users.html#list-ssh-keys

Examples
--------

List SSH keys for a user::

    keys = user.keys.list()

Create an SSH key for a user::

    k = user.keys.create({'title': 'my_key',
                          'key': open('/home/me/.ssh/id_rsa.pub').read()})

Delete an SSH key for a user::

    user.keys.delete(key_id)
    # or
    key.delete()

Status
======

References
----------

You can manipulate the status for the current user and you can read the status of other users.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserStatus`
  + :class:`gitlab.v4.objects.CurrentUserStatusManager`
  + :attr:`gitlab.v4.objects.CurrentUser.status`
  + :class:`gitlab.v4.objects.UserStatus`
  + :class:`gitlab.v4.objects.UserStatusManager`
  + :attr:`gitlab.v4.objects.User.status`

* GitLab API: https://docs.gitlab.com/ce/api/users.html#user-status

Examples
--------

Get current user status::

    status = user.status.get()

Update the status for the current user::

    status = user.status.get()
    status.message = "message"
    status.emoji = "thumbsup"
    status.save()

Get the status of other users::

    gl.users.get(1).status.get()

Emails
======

References
----------

You can manipulate emails for the current user and for the other users if you
are admin.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserEmail`
  + :class:`gitlab.v4.objects.CurrentUserEmailManager`
  + :attr:`gitlab.v4.objects.CurrentUser.emails`
  + :class:`gitlab.v4.objects.UserEmail`
  + :class:`gitlab.v4.objects.UserEmailManager`
  + :attr:`gitlab.v4.objects.User.emails`

* GitLab API: https://docs.gitlab.com/ce/api/users.html#list-emails

Examples
--------

List emails for a user::

    emails = user.emails.list()

Get an email for a user::

    email = user.emails.get(email_id)

Create an email for a user::

    k = user.emails.create({'email': 'foo@bar.com'})

Delete an email for a user::

    user.emails.delete(email_id)
    # or
    email.delete()

Users activities
================

References
----------

* admin only

* v4 API:

  + :class:`gitlab.v4.objects.UserActivities`
  + :class:`gitlab.v4.objects.UserActivitiesManager`
  + :attr:`gitlab.Gitlab.user_activities`

* GitLab API: https://docs.gitlab.com/ce/api/users.html#get-user-activities-admin-only

Examples
--------

Get the users activities::

    activities = gl.user_activities.list(
        query_parameters={'from': '2018-07-01'},
        all=True, as_list=False)

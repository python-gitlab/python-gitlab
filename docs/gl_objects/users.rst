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

* v3 API:

  + :class:`gitlab.v3.objects.User`
  + :class:`gitlab.v3.objects.UserManager`
  + :attr:`gitlab.Gitlab.users`

Examples
--------

Get the list of users:

.. literalinclude:: users.py
   :start-after: # list
   :end-before: # end list

Search users whose username match the given string:

.. literalinclude:: users.py
   :start-after: # search
   :end-before: # end search

Get a single user:

.. literalinclude:: users.py
   :start-after: # get
   :end-before: # end get

Create a user:

.. literalinclude:: users.py
   :start-after: # create
   :end-before: # end create

Update a user:

.. literalinclude:: users.py
   :start-after: # update
   :end-before: # end update

Delete a user:

.. literalinclude:: users.py
   :start-after: # delete
   :end-before: # end delete

Block/Unblock a user:

.. literalinclude:: users.py
   :start-after: # block
   :end-before: # end block

Current User
============

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUser`
  + :class:`gitlab.v4.objects.CurrentUserManager`
  + :attr:`gitlab.Gitlab.user`

* v3 API:

  + :class:`gitlab.v3.objects.CurrentUser`
  + :class:`gitlab.v3.objects.CurrentUserManager`
  + :attr:`gitlab.Gitlab.user`

Examples
--------

Get the current user:

.. literalinclude:: users.py
   :start-after: # currentuser get
   :end-before: # end currentuser get

GPG keys
========

You can manipulate GPG keys for the current user and for the other users if you
are admin.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserGPGKey`
  + :class:`gitlab.v4.objects.CurrentUserGPGKeyManager`
  + :attr:`gitlab.v4.objects.CurrentUser.gpgkeys`
  + :class:`gitlab.v4.objects.UserGPGKey`
  + :class:`gitlab.v4.objects.UserGPGKeyManager`
  + :attr:`gitlab.v4.objects.User.gpgkeys`

Exemples
--------

List GPG keys for a user:

.. literalinclude:: users.py
   :start-after: # gpgkey list
   :end-before: # end gpgkey list

Get an GPG gpgkey for a user:

.. literalinclude:: users.py
   :start-after: # gpgkey get
   :end-before: # end gpgkey get

Create an GPG gpgkey for a user:

.. literalinclude:: users.py
   :start-after: # gpgkey create
   :end-before: # end gpgkey create

Delete an GPG gpgkey for a user:

.. literalinclude:: users.py
   :start-after: # gpgkey delete
   :end-before: # end gpgkey delete

SSH keys
========

You can manipulate SSH keys for the current user and for the other users if you
are admin.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserKey`
  + :class:`gitlab.v4.objects.CurrentUserKeyManager`
  + :attr:`gitlab.v4.objects.CurrentUser.keys`
  + :class:`gitlab.v4.objects.UserKey`
  + :class:`gitlab.v4.objects.UserKeyManager`
  + :attr:`gitlab.v4.objects.User.keys`

* v3 API:

  + :class:`gitlab.v3.objects.CurrentUserKey`
  + :class:`gitlab.v3.objects.CurrentUserKeyManager`
  + :attr:`gitlab.v3.objects.CurrentUser.keys`
  + :attr:`gitlab.Gitlab.user.keys`
  + :class:`gitlab.v3.objects.UserKey`
  + :class:`gitlab.v3.objects.UserKeyManager`
  + :attr:`gitlab.v3.objects.User.keys`
  + :attr:`gitlab.Gitlab.user_keys`

Exemples
--------

List SSH keys for a user:

.. literalinclude:: users.py
   :start-after: # key list
   :end-before: # end key list

Get an SSH key for a user:

.. literalinclude:: users.py
   :start-after: # key get
   :end-before: # end key get

Create an SSH key for a user:

.. literalinclude:: users.py
   :start-after: # key create
   :end-before: # end key create

Delete an SSH key for a user:

.. literalinclude:: users.py
   :start-after: # key delete
   :end-before: # end key delete

Emails
======

You can manipulate emails for the current user and for the other users if you
are admin.

* v4 API:

  + :class:`gitlab.v4.objects.CurrentUserEmail`
  + :class:`gitlab.v4.objects.CurrentUserEmailManager`
  + :attr:`gitlab.v4.objects.CurrentUser.emails`
  + :class:`gitlab.v4.objects.UserEmail`
  + :class:`gitlab.v4.objects.UserEmailManager`
  + :attr:`gitlab.v4.objects.User.emails`

* v3 API:

  + :class:`gitlab.v3.objects.CurrentUserEmail`
  + :class:`gitlab.v3.objects.CurrentUserEmailManager`
  + :attr:`gitlab.v3.objects.CurrentUser.emails`
  + :attr:`gitlab.Gitlab.user.emails`
  + :class:`gitlab.v3.objects.UserEmail`
  + :class:`gitlab.v3.objects.UserEmailManager`
  + :attr:`gitlab.v3.objects.User.emails`
  + :attr:`gitlab.Gitlab.user_emails`

Exemples
--------

List emails for a user:

.. literalinclude:: users.py
   :start-after: # email list
   :end-before: # end email list

Get an email for a user:

.. literalinclude:: users.py
   :start-after: # email get
   :end-before: # end email get

Create an email for a user:

.. literalinclude:: users.py
   :start-after: # email create
   :end-before: # end email create

Delete an email for a user:

.. literalinclude:: users.py
   :start-after: # email delete
   :end-before: # end email delete

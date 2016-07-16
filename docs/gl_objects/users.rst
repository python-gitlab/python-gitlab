#####
Users
#####

Use :class:`~gitlab.objects.User` objects to manipulate repository branches.

To create :class:`~gitlab.objects.User` objects use the
:attr:`gitlab.Gitlab.users` manager.

Examples
========

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

SSH keys
========

Use the :class:`~gitlab.objects.UserKey` objects to manage user keys.

To create :class:`~gitlab.objects.UserKey` objects use the
:attr:`User.keys <gitlab.objects.User.keys>` or :attr:`gitlab.Gitlab.user_keys`
managers.

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

Use the :class:`~gitlab.objects.UserEmail` objects to manage user emails.

To create :class:`~gitlab.objects.UserEmail` objects use the :attr:`User.emails
<gitlab.objects.User.emails>` or :attr:`gitlab.Gitlab.user_emails` managers.

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

Current User
============

Use the :class:`~gitlab.objects.CurrentUser` object to get information about
the currently logged-in user.

Use the :class:`~gitlab.objects.CurrentUserKey` objects to manage user keys.

To create :class:`~gitlab.objects.CurrentUserKey` objects use the
:attr:`gitlab.objects.CurrentUser.keys <CurrentUser.keys>` manager.

Use the :class:`~gitlab.objects.CurrentUserEmail` objects to manage user emails.

To create :class:`~gitlab.objects.CurrentUserEmail` objects use the
:attr:`gitlab.objects.CurrentUser.emails <CurrentUser.emails>` manager.

Examples
--------

Get the current user:

.. literalinclude:: users.py
   :start-after: # currentuser get
   :end-before: # end currentuser get

List the current user SSH keys:

.. literalinclude:: users.py
   :start-after: # currentuser key list
   :end-before: # end currentuser key list

Get a key for the current user:

.. literalinclude:: users.py
   :start-after: # currentuser key get
   :end-before: # end currentuser key get

Create a key for the current user:

.. literalinclude:: users.py
   :start-after: # currentuser key create
   :end-before: # end currentuser key create

Delete a key for the current user:

.. literalinclude:: users.py
   :start-after: # currentuser key delete
   :end-before: # end currentuser key delete

List the current user emails:

.. literalinclude:: users.py
   :start-after: # currentuser email list
   :end-before: # end currentuser email list

Get an email for the current user:

.. literalinclude:: users.py
   :start-after: # currentuser email get
   :end-before: # end currentuser email get

Create an email for the current user:

.. literalinclude:: users.py
   :start-after: # currentuser email create
   :end-before: # end currentuser email create

Delete an email for the current user:

.. literalinclude:: users.py
   :start-after: # currentuser email delete
   :end-before: # end currentuser email delete

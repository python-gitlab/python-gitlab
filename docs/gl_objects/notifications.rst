#####################
Notification settings
#####################

You can define notification settings globally, for groups and for projects.
Valid levels are defined as constants:

* ``NOTIFICATION_LEVEL_DISABLED``
* ``NOTIFICATION_LEVEL_PARTICIPATING``
* ``NOTIFICATION_LEVEL_WATCH``
* ``NOTIFICATION_LEVEL_GLOBAL``
* ``NOTIFICATION_LEVEL_MENTION``
* ``NOTIFICATION_LEVEL_CUSTOM``

You get access to fine-grained settings if you use the
``NOTIFICATION_LEVEL_CUSTOM`` level.

* Object classes: :class:`gitlab.objects.NotificationSettings` (global),
  :class:`gitlab.objects.GroupNotificationSettings` (groups) and
  :class:`gitlab.objects.ProjectNotificationSettings` (projects)
* Manager objects: :attr:`gitlab.Gitlab.notificationsettings` (global),
  :attr:`gitlab.objects.Group.notificationsettings` (groups) and
  :attr:`gitlab.objects.Project.notificationsettings` (projects)

Examples
--------

Get the settings:

.. literalinclude:: notifications.py
   :start-after: # get
   :end-before: # end get

Update the settings:

.. literalinclude:: notifications.py
   :start-after: # update
   :end-before: # end update

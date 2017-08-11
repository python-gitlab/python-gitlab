#####################
Notification settings
#####################

You can define notification settings globally, for groups and for projects.
Valid levels are defined as constants:

* ``gitlab.NOTIFICATION_LEVEL_DISABLED``
* ``gitlab.NOTIFICATION_LEVEL_PARTICIPATING``
* ``gitlab.NOTIFICATION_LEVEL_WATCH``
* ``gitlab.NOTIFICATION_LEVEL_GLOBAL``
* ``gitlab.NOTIFICATION_LEVEL_MENTION``
* ``gitlab.NOTIFICATION_LEVEL_CUSTOM``

You get access to fine-grained settings if you use the
``NOTIFICATION_LEVEL_CUSTOM`` level.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.NotificationSettings`
  + :class:`gitlab.v4.objects.NotificationSettingsManager`
  + :attr:`gitlab.Gitlab.notificationsettings`
  + :class:`gitlab.v4.objects.GroupNotificationSettings`
  + :class:`gitlab.v4.objects.GroupNotificationSettingsManager`
  + :attr:`gitlab.v4.objects.Group.notificationsettings`
  + :class:`gitlab.v4.objects.ProjectNotificationSettings`
  + :class:`gitlab.v4.objects.ProjectNotificationSettingsManager`
  + :attr:`gitlab.v4.objects.Project.notificationsettings`

* v3 API:

  + :class:`gitlab.v3.objects.NotificationSettings`
  + :class:`gitlab.v3.objects.NotificationSettingsManager`
  + :attr:`gitlab.Gitlab.notificationsettings`
  + :class:`gitlab.v3.objects.GroupNotificationSettings`
  + :class:`gitlab.v3.objects.GroupNotificationSettingsManager`
  + :attr:`gitlab.v3.objects.Group.notificationsettings`
  + :class:`gitlab.v3.objects.ProjectNotificationSettings`
  + :class:`gitlab.v3.objects.ProjectNotificationSettingsManager`
  + :attr:`gitlab.v3.objects.Project.notificationsettings`

* GitLab API: https://docs.gitlab.com/ce/api/notification_settings.html

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

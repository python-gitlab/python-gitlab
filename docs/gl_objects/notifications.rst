#####################
Notification settings
#####################

You can define notification settings globally, for groups and for projects.
Valid levels are defined as constants:

* ``gitlab.const.NOTIFICATION_LEVEL_DISABLED``
* ``gitlab.const.NOTIFICATION_LEVEL_PARTICIPATING``
* ``gitlab.const.NOTIFICATION_LEVEL_WATCH``
* ``gitlab.const.NOTIFICATION_LEVEL_GLOBAL``
* ``gitlab.const.NOTIFICATION_LEVEL_MENTION``
* ``gitlab.const.NOTIFICATION_LEVEL_CUSTOM``

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

* GitLab API: https://docs.gitlab.com/ce/api/notification_settings.html

Examples
--------

Get the notifications settings::

    # global settings
    settings = gl.notificationsettings.get()
    # for a group
    settings = gl.groups.get(group_id).notificationsettings.get()
    # for a project
    settings = gl.projects.get(project_id).notificationsettings.get()

Update the notifications settings::

    # use a predefined level
    settings.level = gitlab.const.NOTIFICATION_LEVEL_WATCH

    # create a custom setup
    settings.level = gitlab.const.NOTIFICATION_LEVEL_CUSTOM
    settings.save()  # will create additional attributes, but not mandatory

    settings.new_merge_request = True
    settings.new_issue = True
    settings.new_note = True
    settings.save()

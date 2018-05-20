########
Settings
########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ApplicationSettings`
  + :class:`gitlab.v4.objects.ApplicationSettingsManager`
  + :attr:`gitlab.Gitlab.settings`

* GitLab API: https://docs.gitlab.com/ce/api/settings.html

Examples
--------

Get the settings::

    settings = gl.settings.get()

Update the settings::

    settings.signin_enabled = False
    settings.save()

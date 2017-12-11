########
Settings
########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ApplicationSettings`
  + :class:`gitlab.v4.objects.ApplicationSettingsManager`
  + :attr:`gitlab.Gitlab.settings`

* v3 API:

  + :class:`gitlab.v3.objects.ApplicationSettings`
  + :class:`gitlab.v3.objects.ApplicationSettingsManager`
  + :attr:`gitlab.Gitlab.settings`

* GitLab API: https://docs.gitlab.com/ce/api/settings.html

Examples
--------

Get the settings:

.. literalinclude:: settings.py
   :start-after: # get
   :end-before: # end get

Update the settings:

.. literalinclude:: settings.py
   :start-after: # update
   :end-before: # end update

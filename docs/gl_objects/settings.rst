########
Settings
########

Use :class:`~gitlab.objects.ApplicationSettings` objects to manipulate Gitlab
settings. The :attr:`gitlab.Gitlab.settings` manager object provides helper
functions.

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

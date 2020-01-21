##########
Appearance
##########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ApplicationAppearance`
  + :class:`gitlab.v4.objects.ApplicationAppearanceManager`
  + :attr:`gitlab.Gitlab.appearance`

* GitLab API: https://docs.gitlab.com/ce/api/appearance.html

Examples
--------

Get the appearance::

    appearance = gl.appearance.get()

Update the appearance::

    appearance.title = "Test"
    appearance.save()

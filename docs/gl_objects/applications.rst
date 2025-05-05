############
Applications
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Applications`
  + :class:`gitlab.v4.objects.ApplicationManager`
  + :attr:`gitlab.Gitlab.applications`

* GitLab API: https://docs.gitlab.com/api/applications

Examples
--------

List all OAuth applications::

    applications = gl.applications.list(get_all=True)

Create an application::

    gl.applications.create({'name': 'your_app', 'redirect_uri': 'http://application.url', 'scopes': 'read_user openid profile email'})

Delete an applications::

    gl.applications.delete(app_id)
    # or
    application.delete()

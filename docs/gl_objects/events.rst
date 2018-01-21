######
Events
######

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Event`
  + :class:`gitlab.v4.objects.EventManager`
  + :attr:`gitlab.Gitlab.events`
  + :class:`gitlab.v4.objects.ProjectEvent`
  + :class:`gitlab.v4.objects.ProjectEventManager`
  + :attr:`gitlab.v4.objects.Project.events`
  + :class:`gitlab.v4.objects.UserEvent`
  + :class:`gitlab.v4.objects.UserEventManager`
  + :attr:`gitlab.v4.objects.User.events`

* v3 API (projects events only):

  + :class:`gitlab.v3.objects.ProjectEvent`
  + :class:`gitlab.v3.objects.ProjectEventManager`
  + :attr:`gitlab.v3.objects.Project.events`
  + :attr:`gitlab.Gitlab.project_events`

* GitLab API: https://docs.gitlab.com/ce/api/events.html

Examples
--------

You can list events for an entire Gitlab instance (admin), users and projects.
You can filter you events you want to retrieve using the ``action`` and
``target_type`` attributes. The possibole values for these attributes are
available on `the gitlab documentation
<https://docs.gitlab.com/ce/api/events.html>`_.

List all the events (paginated)::

    events = gl.events.list()

List the issue events on a project::

    events = project.events.list(target_type='issue')

List the user events::

    events = project.events.list()

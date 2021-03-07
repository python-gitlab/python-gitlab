######
Events
######

Events
======

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

* GitLab API: https://docs.gitlab.com/ce/api/events.html

Examples
--------

You can list events for an entire Gitlab instance (admin), users and projects.
You can filter you events you want to retrieve using the ``action`` and
``target_type`` attributes. The possible values for these attributes are
available on `the gitlab documentation
<https://docs.gitlab.com/ce/api/events.html>`_.

List all the events (paginated)::

    events = gl.events.list()

List the issue events on a project::

    events = project.events.list(target_type='issue')

List the user events::

    events = project.events.list()

Resource state events
=====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssueResourceStateEvent`
  + :class:`gitlab.v4.objects.ProjectIssueResourceStateEventManager`
  + :attr:`gitlab.v4.objects.ProjectIssue.resourcestateevents`
  + :class:`gitlab.v4.objects.ProjectMergeRequestResourceStateEvent`
  + :class:`gitlab.v4.objects.ProjectMergeRequestResourceStateEventManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.resourcestateevents`

* GitLab API: https://docs.gitlab.com/ee/api/resource_state_events.html

Examples
--------

You can list and get specific resource state events (via their id) for project issues
and project merge requests.

List the state events of a project issue (paginated)::

    state_events = issue.resourcestateevents.list()

Get a specific state event of a project issue by its id::

    state_event = issue.resourcestateevents.get(1)

List the state events of a project merge request (paginated)::

    state_events = mr.resourcestateevents.list()

Get a specific state event of a project merge request by its id::

    state_event = mr.resourcestateevents.get(1)

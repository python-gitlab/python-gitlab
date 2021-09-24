######
Labels
######

Project labels
==============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectLabel`
  + :class:`gitlab.v4.objects.ProjectLabelManager`
  + :attr:`gitlab.v4.objects.Project.labels`

* GitLab API: https://docs.gitlab.com/ce/api/labels.html

Examples
--------

List labels for a project::

    labels = project.labels.list()

Create a label for a project::

    label = project.labels.create({'name': 'foo', 'color': '#8899aa'})

Update a label for a project::

    # change the name of the label:
    label.new_name = 'bar'
    label.save()
    # change its color:
    label.color = '#112233'
    label.save()

Promote a project label to a group label::

    label.promote()

Delete a label for a project::

    project.labels.delete(label_id)
    # or
    label.delete()

Manage labels in issues and merge requests::

    # Labels are defined as lists in issues and merge requests. The labels must
    # exist.
    issue = p.issues.create({'title': 'issue title',
                             'description': 'issue description',
                             'labels': ['foo']})
    issue.labels.append('bar')
    issue.save()

Label events
============

Resource label events keep track about who, when, and which label was added or
removed to an issuable.

Group epic label events are only available in the EE edition.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssueResourceLabelEvent`
  + :class:`gitlab.v4.objects.ProjectIssueResourceLabelEventManager`
  + :attr:`gitlab.v4.objects.ProjectIssue.resourcelabelevents`
  + :class:`gitlab.v4.objects.ProjectMergeRequestResourceLabelEvent`
  + :class:`gitlab.v4.objects.ProjectMergeRequestResourceLabelEventManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.resourcelabelevents`
  + :class:`gitlab.v4.objects.GroupEpicResourceLabelEvent`
  + :class:`gitlab.v4.objects.GroupEpicResourceLabelEventManager`
  + :attr:`gitlab.v4.objects.GroupEpic.resourcelabelevents`

* GitLab API: https://docs.gitlab.com/ee/api/resource_label_events.html

Examples
--------

Get the events for a resource (issue, merge request or epic)::

    events = resource.resourcelabelevents.list()

Get a specific event for a resource::

    event = resource.resourcelabelevents.get(event_id)

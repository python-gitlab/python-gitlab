######
Labels
######

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

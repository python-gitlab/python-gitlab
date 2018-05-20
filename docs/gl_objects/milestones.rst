##########
Milestones
##########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMilestone`
  + :class:`gitlab.v4.objects.ProjectMilestoneManager`
  + :attr:`gitlab.v4.objects.Project.milestones`

  + :class:`gitlab.v4.objects.GroupMilestone`
  + :class:`gitlab.v4.objects.GroupMilestoneManager`
  + :attr:`gitlab.v4.objects.Group.milestones`

* GitLab API:

  + https://docs.gitlab.com/ce/api/milestones.html
  + https://docs.gitlab.com/ce/api/group_milestones.html

Examples
--------

List the milestones for a project or a group::

    p_milestones = project.milestones.list()
    g_milestones = group.milestones.list()

You can filter the list using the following parameters:

* ``iid``: unique ID of the milestone for the project
* ``state``: either ``active`` or ``closed``
* ``search``: to search using a string

::

    p_milestones = project.milestones.list(state='closed')
    g_milestones = group.milestones.list(state='active')

Get a single milestone::

    p_milestone = project.milestones.get(milestone_id)
    g_milestone = group.milestones.get(milestone_id)

Create a milestone::

    milestone = project.milestones.create({'title': '1.0'})

Edit a milestone::

    milestone.description = 'v 1.0 release'
    milestone.save()

Change the state of a milestone (activate / close)::

    # close a milestone
    milestone.state_event = 'close'
    milestone.save()

    # activate a milestone
    milestone.state_event = 'activate'
    milestone.save()

List the issues related to a milestone::

    issues = milestone.issues()

List the merge requests related to a milestone::

    merge_requests = milestone.merge_requests()

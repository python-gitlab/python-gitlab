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

* v3 API:

  + :class:`gitlab.v3.objects.ProjectMilestone`
  + :class:`gitlab.v3.objects.ProjectMilestoneManager`
  + :attr:`gitlab.v3.objects.Project.milestones`
  + :attr:`gitlab.Gitlab.project_milestones`

* GitLab API:

  + https://docs.gitlab.com/ce/api/milestones.html
  + https://docs.gitlab.com/ce/api/group_milestones.html

Examples
--------

List the milestones for a project or a group:

.. literalinclude:: milestones.py
   :start-after: # list
   :end-before: # end list

You can filter the list using the following parameters:

* ``iid``: unique ID of the milestone for the project
* ``state``: either ``active`` or ``closed``
* ``search``: to search using a string

.. literalinclude:: milestones.py
   :start-after: # filter
   :end-before: # end filter

Get a single milestone:

.. literalinclude:: milestones.py
   :start-after: # get
   :end-before: # end get

Create a milestone:

.. literalinclude:: milestones.py
   :start-after: # create
   :end-before: # end create

Edit a milestone:

.. literalinclude:: milestones.py
   :start-after: # update
   :end-before: # end update

Change the state of a milestone (activate / close):

.. literalinclude:: milestones.py
   :start-after: # state
   :end-before: # end state

List the issues related to a milestone:

.. literalinclude:: milestones.py
   :start-after: # issues
   :end-before: # end issues

List the merge requests related to a milestone:

.. literalinclude:: milestones.py
   :start-after: # merge_requests
   :end-before: # end merge_requests

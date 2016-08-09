##########
Milestones
##########

Use :class:`~gitlab.objects.ProjectMilestone` objects to manipulate milestones.
The :attr:`gitlab.Gitlab.project_milestones` and :attr:`Project.milestones
<gitlab.objects.Project.milestones>` manager objects provide helper functions.

Examples
--------

List the milestones for a project:

.. literalinclude:: milestones.py
   :start-after: # list
   :end-before: # end list

You can filter the list using the following parameters:

* ``iid``: unique ID of the milestone for the project
* ``state``: either ``active`` or ``closed``

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

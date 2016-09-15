########
Branches
########

Use :class:`~gitlab.objects.ProjectBranch` objects to manipulate repository
branches.

To create :class:`~gitlab.objects.ProjectBranch` objects use the
:attr:`gitlab.Gitlab.project_branches` or :attr:`Project.branches
<gitlab.objects.Project.branches>` managers.

Examples
========

Get the list of branches for a repository:

.. literalinclude:: branches.py
   :start-after: # list
   :end-before: # end list

Get a single repository branch:

.. literalinclude:: branches.py
   :start-after: # get
   :end-before: # end get

Create a repository branch:

.. literalinclude:: branches.py
   :start-after: # create
   :end-before: # end create

Delete a repository branch:

.. literalinclude:: branches.py
   :start-after: # delete
   :end-before: # end delete

Protect/unprotect a repository branch:

.. literalinclude:: branches.py
   :start-after: # protect
   :end-before: # end protect
   
.. note::
   
   By default, developers will not be able to push or merge into
   protected branches. This can be changed by passing ``developers_can_push``
   or ``developers_can_merge`` like so: 
   ``branch.protect(developers_can_push=False, developers_can_merge=True)``

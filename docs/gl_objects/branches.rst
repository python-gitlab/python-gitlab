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

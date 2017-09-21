##################
Protected branches
##################

You can define a list of protected branch names on a repository. Names can use
wildcards (``*``).

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectProtectedBranch`
  + :class:`gitlab.v4.objects.ProjectProtectedBranchManager`
  + :attr:`gitlab.v4.objects.Project.protectedbranches`

* GitLab API: https://docs.gitlab.com/ce/api/protected_branches.html#protected-branches-api

Examples
--------

Get the list of protected branches for a project:

.. literalinclude:: branches.py
   :start-after: # p_branch list
   :end-before: # end p_branch list

Get a single protected branch:

.. literalinclude:: branches.py
   :start-after: # p_branch get
   :end-before: # end p_branch get

Create a protected branch:

.. literalinclude:: branches.py
   :start-after: # p_branch create
   :end-before: # end p_branch create

Delete a protected branch:

.. literalinclude:: branches.py
   :start-after: # p_branch delete
   :end-before: # end p_branch delete

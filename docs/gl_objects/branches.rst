########
Branches
########

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectBranch`
  + :class:`gitlab.v4.objects.ProjectBranchManager`
  + :attr:`gitlab.v4.objects.Project.branches`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectBranch`
  + :class:`gitlab.v3.objects.ProjectBranchManager`
  + :attr:`gitlab.v3.objects.Project.branches`

* GitLab API: https://docs.gitlab.com/ce/api/branches.html

Examples
--------

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

   By default, developers are not authorized to push or merge into protected
   branches. This can be changed by passing ``developers_can_push`` or
   ``developers_can_merge``:

   .. code-block:: python

      branch.protect(developers_can_push=True, developers_can_merge=True)

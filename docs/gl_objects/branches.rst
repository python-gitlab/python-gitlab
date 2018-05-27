########
Branches
########

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectBranch`
  + :class:`gitlab.v4.objects.ProjectBranchManager`
  + :attr:`gitlab.v4.objects.Project.branches`

* GitLab API: https://docs.gitlab.com/ce/api/branches.html

Examples
--------

Get the list of branches for a repository::

    branches = project.branches.list()

Get a single repository branch::

    branch = project.branches.get('master')

Create a repository branch::

    branch = project.branches.create({'branch': 'feature1',
                                      'ref': 'master'})

Delete a repository branch::

    project.branches.delete('feature1')
    # or
    branch.delete()

Protect/unprotect a repository branch::

    branch.protect()
    branch.unprotect()

.. note::

   By default, developers are not authorized to push or merge into protected
   branches. This can be changed by passing ``developers_can_push`` or
   ``developers_can_merge``:

   .. code-block:: python

      branch.protect(developers_can_push=True, developers_can_merge=True)

Delete the merged branches for a project::

    project.delete_merged_branches()

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
Branch listing uses the base ListMixin class which provides pagination.

Get a list of branches for a repository (Limited to 20 branches in a pagination response)::

    branches = project.branches.list()
    
Get a list of ALL branches for a repository::

    branches = project.branches.list(all=True)    

Get a single repository branch::

    branch = project.branches.get('main')

Create a repository branch::

    branch = project.branches.create({'branch': 'feature1',
                                      'ref': 'main'})

Delete a repository branch::

    project.branches.delete('feature1')
    # or
    branch.delete()

Delete the merged branches for a project::

    project.delete_merged_branches()

To manage protected branches, see :doc:`/gl_objects/protected_branches`.

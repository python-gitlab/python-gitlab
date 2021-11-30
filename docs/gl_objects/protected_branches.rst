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

Get the list of protected branches for a project::

    p_branches = project.protectedbranches.list()

Get a single protected branch::

    p_branch = project.protectedbranches.get('main')

Create a protected branch::

    p_branch = project.protectedbranches.create({
        'name': '*-stable',
        'merge_access_level': gitlab.const.DEVELOPER_ACCESS,
        'push_access_level': gitlab.const.MAINTAINER_ACCESS
    })

Create a protected branch with more granular access control::

    p_branch = project.protectedbranches.create({
        'name': '*-stable',
        'allowed_to_push': [{"user_id": 99}, {"user_id": 98}],
        'allowed_to_merge': [{"group_id": 653}],
        'allowed_to_unprotect': [{"access_level": gitlab.const.MAINTAINER_ACCESS}]
    })

Delete a protected branch::

    project.protectedbranches.delete('*-stable')
    # or
    p_branch.delete()

#######################
External Status Checks
#######################

Manage external status checks for projects and merge requests.


Project external status checks
===============================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectExternalStatusCheck`
  + :class:`gitlab.v4.objects.ProjectExternalStatusCheckManager`
  + :attr:`gitlab.v4.objects.Project.external_status_checks`

* GitLab API: https://docs.gitlab.com/api/status_checks

Examples
---------

List external status checks for a project::

    status_checks = project.external_status_checks.list(get_all=True)

Create an external status check with shared secret::

    status_checks = project.external_status_checks.create({
        "name": "mr_blocker",
        "external_url": "https://example.com/mr-status-check",
        "shared_secret": "secret-string"
    })

Create an external status check with shared secret for protected branches::

    protected_branch = project.protectedbranches.get('main')

    status_check = project.external_status_checks.create({
        "name": "mr_blocker",
        "external_url": "https://example.com/mr-status-check",
        "shared_secret": "secret-string",
        "protected_branch_ids": [protected_branch.id]
    })


Update an external status check::

    status_check.external_url = "https://example.com/mr-blocker"
    status_check.save()

Delete an external status check::

    status_check.delete(status_check_id)


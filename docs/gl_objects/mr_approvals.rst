#######################
Merge request approvals
#######################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeRequestApproval`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalManager`
  + :attr:`gitlab.v4.objects.Project.approvals`

* GitLab API: https://docs.gitlab.com/ce/api/merge_request_approvals.html

Examples
--------

Get project-level MR approvals configuration::

    mrac = project.approvals.get()

Change project-level MR approvals configuration::

    mrac.approvals_before_merge = 2
    mrac.save()

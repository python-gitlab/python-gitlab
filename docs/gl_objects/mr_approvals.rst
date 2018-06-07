##############################################
Project-level merge request approvals settings
##############################################

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalSettings`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalSettingsManager`
  + :attr:`gitlab.v4.objects.Project.approvalsettings`

* GitLab API: https://docs.gitlab.com/ee/api/merge_request_approvals.html#project-level-mr-approvals

Examples
--------

Get project-level MR approvals settings::

    mras = project.approvalsettings.get()

Change project-level MR approvals settings::

    mras.approvals_before_merge = 2
    mras.save()

Change project-level MR allowed approvers::

	project.approvalsettings.set_approvers(approver_ids = [105], approver_group_ids=[653, 654])

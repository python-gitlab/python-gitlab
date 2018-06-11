################################
Merge request approvals settings
################################

Merge request approvals can be defined at the project level or at the merge
request level.

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectApproval`
  + :class:`gitlab.v4.objects.ProjectApprovalManager`
  + :attr:`gitlab.v4.objects.Project.approvals`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApproval`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.approvals`

* GitLab API: https://docs.gitlab.com/ee/api/merge_request_approvals.html

Examples
--------

Get project-level or MR-level MR approvals settings::

    p_mras = project.approvals.get()

    mr_mras = mr.approvals.get()

Change project-level or MR-level MR approvals settings::

    p_mras.approvals_before_merge = 2
    p_mras.save()

    mr_mras.approvals_before_merge = 2
    mr_mras.save()

Change project-level or MR-level MR allowed approvers::

	project.approvals.set_approvers(approver_ids=[105],
                                    approver_group_ids=[653, 654])

	mr.approvals.set_approvers(approver_ids=[105],
                               approver_group_ids=[653, 654])

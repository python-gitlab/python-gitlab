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
  + :class:`gitlab.v4.objects.ProjectApprovalRule`
  + :class:`gitlab.v4.objects.ProjectApprovalRuleManager`
  + :attr:`gitlab.v4.objects.Project.approvals`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApproval`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.approvals`

* GitLab API: https://docs.gitlab.com/ee/api/merge_request_approvals.html

Examples
--------

List project-level MR approval rules::

    p_mras = project.approvalrules.list()

Change project-level MR approval rule::

    p_approvalrule.user_ids = [234]
    p_approvalrule.save()

Delete project-level MR approval rule::

    p_approvalrule.delete()

Get project-level or MR-level MR approvals settings::

    p_mras = project.approvals.get()

    mr_mras = mr.approvals.get()

Change project-level or MR-level MR approvals settings::

    p_mras.approvals_before_merge = 2
    p_mras.save()

    mr_mras.set_approvers(approvals_required = 1)

Change project-level or MR-level MR allowed approvers::

	project.approvals.set_approvers(approver_ids=[105],
                                    approver_group_ids=[653, 654])

	mr.approvals.set_approvers(approvals_required = 1, approver_ids=[105],
                               approver_group_ids=[653, 654])

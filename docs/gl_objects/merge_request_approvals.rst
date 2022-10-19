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
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalRule`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalRuleManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.approval_rules`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalState`
  + :class:`gitlab.v4.objects.ProjectMergeRequestApprovalStateManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.approval_state`

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

Get MR-level approval state::

    mr_approval_state = mr.approval_state.get()

Change project-level or MR-level MR approvals settings::

    p_mras.approvals_before_merge = 2
    p_mras.save()

    mr.approvals.set_approvers(approvals_required=1)
    # or
    mr_mras.approvals_required = 1
    mr_mras.save()

Create a new MR-level approval rule or change an existing MR-level approval rule::

    mr.approvals.set_approvers(approvals_required = 1, approver_ids=[105],
                               approver_group_ids=[653, 654],
                               approval_rule_name="my MR custom approval rule")

List MR-level MR approval rules::

    mr.approval_rules.list()

Get a single MR approval rule::

    approval_rule_id = 123
    mr_approvalrule = mr.approval_rules.get(approval_rule_id)

Delete MR-level MR approval rule::

    rules = mr.approval_rules.list()
    rules[0].delete()

    # or
    mr.approval_rules.delete(approval_id)

Change MR-level MR approval rule::

    mr_approvalrule.user_ids = [105]
    mr_approvalrule.approvals_required = 2
    mr_approvalrule.group_ids = [653, 654]
    mr_approvalrule.save()

Create a MR-level MR approval rule::

   mr.approval_rules.create({
       "name": "my MR custom approval rule",
       "approvals_required": 2,
       "rule_type": "regular",
       "user_ids": [105],
       "group_ids": [653, 654],
   })

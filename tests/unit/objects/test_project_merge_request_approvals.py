"""
Gitlab API: https://docs.gitlab.com/ee/api/merge_request_approvals.html
"""

import copy

import pytest
import responses

import gitlab

approval_rule_id = 1
approval_rule_name = "security"
approvals_required = 3
user_ids = [5, 50]
group_ids = [5]

new_approval_rule_name = "new approval rule"
new_approval_rule_user_ids = user_ids
new_approval_rule_approvals_required = 2

updated_approval_rule_user_ids = [5]
updated_approval_rule_approvals_required = 1


@pytest.fixture
def resp_snippet():
    merge_request_content = [
        {
            "id": 1,
            "iid": 1,
            "project_id": 1,
            "title": "test1",
            "description": "fixed login page css paddings",
            "state": "merged",
            "merged_by": {
                "id": 87854,
                "name": "Douwe Maan",
                "username": "DouweM",
                "state": "active",
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
                "web_url": "https://gitlab.com/DouweM",
            },
            "merged_at": "2018-09-07T11:16:17.520Z",
            "closed_by": None,
            "closed_at": None,
            "created_at": "2017-04-29T08:46:00Z",
            "updated_at": "2017-04-29T08:46:00Z",
            "target_branch": "main",
            "source_branch": "test1",
            "upvotes": 0,
            "downvotes": 0,
            "author": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignee": {
                "id": 1,
                "name": "Administrator",
                "username": "admin",
                "state": "active",
                "avatar_url": None,
                "web_url": "https://gitlab.example.com/admin",
            },
            "assignees": [
                {
                    "name": "Miss Monserrate Beier",
                    "username": "axel.block",
                    "id": 12,
                    "state": "active",
                    "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
                    "web_url": "https://gitlab.example.com/axel.block",
                }
            ],
            "source_project_id": 2,
            "target_project_id": 3,
            "labels": ["Community contribution", "Manage"],
            "work_in_progress": None,
            "milestone": {
                "id": 5,
                "iid": 1,
                "project_id": 3,
                "title": "v2.0",
                "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
                "state": "closed",
                "created_at": "2015-02-02T19:49:26.013Z",
                "updated_at": "2015-02-02T19:49:26.013Z",
                "due_date": "2018-09-22",
                "start_date": "2018-08-08",
                "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1",
            },
            "merge_when_pipeline_succeeds": None,
            "merge_status": "can_be_merged",
            "sha": "8888888888888888888888888888888888888888",
            "merge_commit_sha": None,
            "squash_commit_sha": None,
            "user_notes_count": 1,
            "discussion_locked": None,
            "should_remove_source_branch": True,
            "force_remove_source_branch": False,
            "allow_collaboration": False,
            "allow_maintainer_to_push": False,
            "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
            "references": {
                "short": "!1",
                "relative": "my-group/my-project!1",
                "full": "my-group/my-project!1",
            },
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "squash": False,
            "task_completion_status": {"count": 0, "completed_count": 0},
        }
    ]
    mr_ars_content = [
        {
            "id": approval_rule_id,
            "name": approval_rule_name,
            "rule_type": "regular",
            "eligible_approvers": [
                {
                    "id": user_ids[0],
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                },
                {
                    "id": user_ids[1],
                    "name": "Group Member 1",
                    "username": "group_member_1",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/group_member_1",
                },
            ],
            "approvals_required": approvals_required,
            "source_rule": None,
            "users": [
                {
                    "id": 5,
                    "name": "John Doe",
                    "username": "jdoe",
                    "state": "active",
                    "avatar_url": "https://www.gravatar.com/avatar/0?s=80&d=identicon",
                    "web_url": "http://localhost/jdoe",
                }
            ],
            "groups": [
                {
                    "id": 5,
                    "name": "group1",
                    "path": "group1",
                    "description": "",
                    "visibility": "public",
                    "lfs_enabled": False,
                    "avatar_url": None,
                    "web_url": "http://localhost/groups/group1",
                    "request_access_enabled": False,
                    "full_name": "group1",
                    "full_path": "group1",
                    "parent_id": None,
                    "ldap_cn": None,
                    "ldap_access": None,
                }
            ],
            "contains_hidden_groups": False,
            "overridden": False,
        }
    ]

    approval_state_rules = copy.deepcopy(mr_ars_content)
    approval_state_rules[0]["approved"] = False
    approval_state_rules[0]["approved_by"] = []

    mr_approval_state_content = {
        "approval_rules_overwritten": False,
        "rules": approval_state_rules,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests",
            json=merge_request_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1",
            json=merge_request_content[0],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/approval_rules",
            json=mr_ars_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/approval_state",
            json=mr_approval_state_content,
            content_type="application/json",
            status=200,
        )

        new_mr_ars_content = dict(mr_ars_content[0])
        new_mr_ars_content["name"] = new_approval_rule_name
        new_mr_ars_content["approvals_required"] = new_approval_rule_approvals_required

        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/merge_requests/1/approval_rules",
            json=new_mr_ars_content,
            content_type="application/json",
            status=200,
        )

        updated_mr_ars_content = copy.deepcopy(mr_ars_content[0])
        updated_mr_ars_content["eligible_approvers"] = [
            mr_ars_content[0]["eligible_approvers"][0]
        ]

        updated_mr_ars_content[
            "approvals_required"
        ] = updated_approval_rule_approvals_required

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/merge_requests/1/approval_rules/1",
            json=updated_mr_ars_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_project_approval_manager_update_uses_post(project, resp_snippet):
    """Ensure the
    gitlab.v4.objects.merge_request_approvals.ProjectApprovalManager object has
    _update_uses_post set to True"""
    approvals = project.approvals
    assert isinstance(
        approvals, gitlab.v4.objects.merge_request_approvals.ProjectApprovalManager
    )
    assert approvals._update_uses_post is True


def test_list_merge_request_approval_rules(project, resp_snippet):
    approval_rules = project.mergerequests.get(1).approval_rules.list()
    assert len(approval_rules) == 1
    assert approval_rules[0].name == approval_rule_name
    assert approval_rules[0].id == approval_rule_id


def test_update_merge_request_approvals_set_approvers(project, resp_snippet):
    approvals = project.mergerequests.get(1).approvals
    assert isinstance(
        approvals,
        gitlab.v4.objects.merge_request_approvals.ProjectMergeRequestApprovalManager,
    )
    assert approvals._update_uses_post is True
    response = approvals.set_approvers(
        updated_approval_rule_approvals_required,
        approver_ids=updated_approval_rule_user_ids,
        approver_group_ids=group_ids,
        approval_rule_name=approval_rule_name,
    )

    assert response.approvals_required == updated_approval_rule_approvals_required
    assert len(response.eligible_approvers) == len(updated_approval_rule_user_ids)
    assert response.eligible_approvers[0]["id"] == updated_approval_rule_user_ids[0]
    assert response.name == approval_rule_name


def test_create_merge_request_approvals_set_approvers(project, resp_snippet):
    approvals = project.mergerequests.get(1).approvals
    assert isinstance(
        approvals,
        gitlab.v4.objects.merge_request_approvals.ProjectMergeRequestApprovalManager,
    )
    assert approvals._update_uses_post is True
    response = approvals.set_approvers(
        new_approval_rule_approvals_required,
        approver_ids=new_approval_rule_user_ids,
        approver_group_ids=group_ids,
        approval_rule_name=new_approval_rule_name,
    )
    assert response.approvals_required == new_approval_rule_approvals_required
    assert len(response.eligible_approvers) == len(new_approval_rule_user_ids)
    assert response.eligible_approvers[0]["id"] == new_approval_rule_user_ids[0]
    assert response.name == new_approval_rule_name


def test_create_merge_request_approval_rule(project, resp_snippet):
    approval_rules = project.mergerequests.get(1).approval_rules
    data = {
        "name": new_approval_rule_name,
        "approvals_required": new_approval_rule_approvals_required,
        "rule_type": "regular",
        "user_ids": new_approval_rule_user_ids,
        "group_ids": group_ids,
    }
    response = approval_rules.create(data)
    assert response.approvals_required == new_approval_rule_approvals_required
    assert len(response.eligible_approvers) == len(new_approval_rule_user_ids)
    assert response.eligible_approvers[0]["id"] == new_approval_rule_user_ids[0]
    assert response.name == new_approval_rule_name


def test_update_merge_request_approval_rule(project, resp_snippet):
    approval_rules = project.mergerequests.get(1).approval_rules
    ar_1 = approval_rules.list()[0]
    ar_1.user_ids = updated_approval_rule_user_ids
    ar_1.approvals_required = updated_approval_rule_approvals_required
    ar_1.save()

    assert ar_1.approvals_required == updated_approval_rule_approvals_required
    assert len(ar_1.eligible_approvers) == len(updated_approval_rule_user_ids)
    assert ar_1.eligible_approvers[0]["id"] == updated_approval_rule_user_ids[0]


def test_get_merge_request_approval_state(project, resp_snippet):
    merge_request = project.mergerequests.get(1)
    approval_state = merge_request.approval_state.get()
    assert isinstance(
        approval_state,
        gitlab.v4.objects.merge_request_approvals.ProjectMergeRequestApprovalState,
    )
    assert not approval_state.approval_rules_overwritten
    assert len(approval_state.rules) == 1
    assert approval_state.rules[0]["name"] == approval_rule_name
    assert approval_state.rules[0]["id"] == approval_rule_id
    assert not approval_state.rules[0]["approved"]
    assert approval_state.rules[0]["approved_by"] == []

"""
Gitlab API: https://docs.gitlab.com/ee/api/merge_request_approvals.html
"""

import copy

import pytest
import responses

import gitlab
from gitlab.mixins import UpdateMethod

approval_rule_id = 7
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
def resp_prj_approval_rules():
    prj_ars_content = [
        {
            "id": approval_rule_id,
            "name": approval_rule_name,
            "rule_type": "regular",
            "report_type": None,
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
            "applies_to_all_protected_branches": False,
            "protected_branches": [
                {
                    "id": 1,
                    "name": "main",
                    "push_access_levels": [
                        {
                            "access_level": 30,
                            "access_level_description": "Developers + Maintainers",
                        }
                    ],
                    "merge_access_levels": [
                        {
                            "access_level": 30,
                            "access_level_description": "Developers + Maintainers",
                        }
                    ],
                    "unprotect_access_levels": [
                        {"access_level": 40, "access_level_description": "Maintainers"}
                    ],
                    "code_owner_approval_required": "false",
                }
            ],
            "contains_hidden_groups": False,
        }
    ]

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/approval_rules",
            json=prj_ars_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/approval_rules/7",
            json=prj_ars_content[0],
            content_type="application/json",
            status=200,
        )

        new_prj_ars_content = dict(prj_ars_content[0])
        new_prj_ars_content["name"] = new_approval_rule_name
        new_prj_ars_content["approvals_required"] = new_approval_rule_approvals_required

        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/approval_rules",
            json=new_prj_ars_content,
            content_type="application/json",
            status=200,
        )

        updated_mr_ars_content = copy.deepcopy(prj_ars_content[0])
        updated_mr_ars_content["eligible_approvers"] = [
            prj_ars_content[0]["eligible_approvers"][0]
        ]

        updated_mr_ars_content["approvals_required"] = (
            updated_approval_rule_approvals_required
        )

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/approval_rules/7",
            json=updated_mr_ars_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_mr_approval_rules():
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
            url="http://localhost/api/v4/projects/1/merge_requests/3/approval_rules",
            json=mr_ars_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/3/approval_rules/7",
            json=mr_ars_content[0],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/3/approval_state",
            json=mr_approval_state_content,
            content_type="application/json",
            status=200,
        )

        new_mr_ars_content = dict(mr_ars_content[0])
        new_mr_ars_content["name"] = new_approval_rule_name
        new_mr_ars_content["approvals_required"] = new_approval_rule_approvals_required

        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/merge_requests/3/approval_rules",
            json=new_mr_ars_content,
            content_type="application/json",
            status=200,
        )

        updated_mr_ars_content = copy.deepcopy(mr_ars_content[0])
        updated_mr_ars_content["eligible_approvers"] = [
            mr_ars_content[0]["eligible_approvers"][0]
        ]

        updated_mr_ars_content["approvals_required"] = (
            updated_approval_rule_approvals_required
        )

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/merge_requests/3/approval_rules/7",
            json=updated_mr_ars_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_mr_approval_rule():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/merge_requests/3/approval_rules/7",
            status=204,
        )
        yield rsps


def test_project_approval_manager_update_method_post(project):
    """Ensure the
    gitlab.v4.objects.merge_request_approvals.ProjectApprovalManager object has
    _update_method set to UpdateMethod.POST"""
    approvals = project.approvals
    assert isinstance(
        approvals, gitlab.v4.objects.merge_request_approvals.ProjectApprovalManager
    )
    assert approvals._update_method is UpdateMethod.POST


def test_list_project_approval_rules(project, resp_prj_approval_rules):
    approval_rules = project.approvalrules.list()
    assert len(approval_rules) == 1
    assert approval_rules[0].name == approval_rule_name
    assert approval_rules[0].id == approval_rule_id
    assert (
        repr(approval_rules[0])
        == f"<ProjectApprovalRule id:{approval_rule_id} name:{approval_rule_name}>"
    )


def test_list_merge_request_approval_rules(project, resp_mr_approval_rules):
    approval_rules = project.mergerequests.get(3, lazy=True).approval_rules.list()
    assert len(approval_rules) == 1
    assert approval_rules[0].name == approval_rule_name
    assert approval_rules[0].id == approval_rule_id
    repr(approval_rules)  # ensure that `repr()` doesn't raise an exception


def test_delete_merge_request_approval_rule(project, resp_delete_mr_approval_rule):
    merge_request = project.mergerequests.get(3, lazy=True)
    merge_request.approval_rules.delete(approval_rule_id)


def test_update_merge_request_approvals_set_approvers(project, resp_mr_approval_rules):
    approvals = project.mergerequests.get(3, lazy=True).approvals
    assert isinstance(
        approvals,
        gitlab.v4.objects.merge_request_approvals.ProjectMergeRequestApprovalManager,
    )
    assert approvals._update_method is UpdateMethod.POST
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


def test_create_merge_request_approvals_set_approvers(project, resp_mr_approval_rules):
    approvals = project.mergerequests.get(3, lazy=True).approvals
    assert isinstance(
        approvals,
        gitlab.v4.objects.merge_request_approvals.ProjectMergeRequestApprovalManager,
    )
    assert approvals._update_method is UpdateMethod.POST
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


def test_create_merge_request_approval_rule(project, resp_mr_approval_rules):
    approval_rules = project.mergerequests.get(3, lazy=True).approval_rules
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


def test_update_merge_request_approval_rule(project, resp_mr_approval_rules):
    approval_rules = project.mergerequests.get(3, lazy=True).approval_rules
    ar_1 = approval_rules.list()[0]
    ar_1.user_ids = updated_approval_rule_user_ids
    ar_1.approvals_required = updated_approval_rule_approvals_required
    ar_1.save()

    assert ar_1.approvals_required == updated_approval_rule_approvals_required
    assert len(ar_1.eligible_approvers) == len(updated_approval_rule_user_ids)
    assert ar_1.eligible_approvers[0]["id"] == updated_approval_rule_user_ids[0]


def test_get_merge_request_approval_rule(project, resp_mr_approval_rules):
    merge_request = project.mergerequests.get(3, lazy=True)
    approval_rule = merge_request.approval_rules.get(approval_rule_id)
    assert isinstance(
        approval_rule,
        gitlab.v4.objects.merge_request_approvals.ProjectMergeRequestApprovalRule,
    )
    assert approval_rule.name == approval_rule_name
    assert approval_rule.id == approval_rule_id


def test_get_merge_request_approval_state(project, resp_mr_approval_rules):
    merge_request = project.mergerequests.get(3, lazy=True)
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

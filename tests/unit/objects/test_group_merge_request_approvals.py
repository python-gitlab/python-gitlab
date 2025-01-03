"""
Gitlab API: https://docs.gitlab.com/ee/api/merge_request_approvals.html
"""

import copy
import json

import pytest
import responses

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
def resp_group_approval_rules():
    content = [
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

    new_content = dict(content[0])
    new_content["id"] = approval_rule_id + 1  # Assign a new ID for the new rule
    new_content["name"] = new_approval_rule_name
    new_content["approvals_required"] = new_approval_rule_approvals_required

    updated_mr_ars_content = copy.deepcopy(content[0])
    updated_mr_ars_content["name"] = new_approval_rule_name
    updated_mr_ars_content["approvals_required"] = (
        updated_approval_rule_approvals_required
    )

    list_request_options = {
        "include_newly_created_rule": False,
        "updated_first_rule": False,
    }

    def list_request_callback(request):
        if request.method == "GET":
            if list_request_options["include_newly_created_rule"]:
                # Include newly created rule in the list response
                return (
                    200,
                    {"Content-Type": "application/json"},
                    json.dumps(content + [new_content]),
                )
            elif list_request_options["updated_first_rule"]:
                # Include updated first rule in the list response
                return (
                    200,
                    {"Content-Type": "application/json"},
                    json.dumps([updated_mr_ars_content]),
                )
            else:
                return (200, {"Content-Type": "application/json"}, json.dumps(content))
        return (404, {}, "")

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        # Mock the API responses for listing all rules for group with ID 1
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/approval_rules",
            json=content,
            content_type="application/json",
            status=200,
        )
        # Mock the API responses for listing all rules for group with ID 1
        # Use a callback to dynamically determine the response based on the request
        rsps.add_callback(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/approval_rules",
            callback=list_request_callback,
            content_type="application/json",
        )
        # Mock the API responses for getting a specific rule for group with ID 1 and approvalrule with ID 7
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/approval_rules/7",
            json=content[0],
            content_type="application/json",
            status=200,
        )
        # Mock the API responses for creating a new rule for group with ID 1
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/approval_rules",
            json=new_content,
            content_type="application/json",
            status=200,
        )
        # Mock the API responses for updating a specific rule for group with ID 1 and approval rule with ID 7
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/groups/1/approval_rules/7",
            json=updated_mr_ars_content,
            content_type="application/json",
            status=200,
        )

        yield rsps, list_request_options


def test_list_group_mr_approval_rules(group, resp_group_approval_rules):
    approval_rules = group.approval_rules.list()
    assert len(approval_rules) == 1
    assert approval_rules[0].name == approval_rule_name
    assert approval_rules[0].id == approval_rule_id
    assert (
        repr(approval_rules[0])
        == f"<GroupApprovalRule id:{approval_rule_id} name:{approval_rule_name}>"
    )


def test_save_group_mr_approval_rule(group, resp_group_approval_rules):
    _, list_request_options = resp_group_approval_rules

    # Before: existing approval rule
    approval_rules = group.approval_rules.list()
    assert len(approval_rules) == 1
    assert approval_rules[0].name == approval_rule_name

    rule_to_be_changed = group.approval_rules.get(approval_rules[0].id)
    rule_to_be_changed.name = new_approval_rule_name
    rule_to_be_changed.approvals_required = new_approval_rule_approvals_required
    rule_to_be_changed.save()

    # Set the flag to return updated rule in the list response
    list_request_options["updated_first_rule"] = True

    # After: changed approval rule
    approval_rules = group.approval_rules.list()
    assert len(approval_rules) == 1
    assert approval_rules[0].name == new_approval_rule_name
    assert (
        repr(approval_rules[0])
        == f"<GroupApprovalRule id:{approval_rule_id} name:{new_approval_rule_name}>"
    )


def test_create_group_mr_approval_rule(group, resp_group_approval_rules):
    _, list_request_options = resp_group_approval_rules

    # Before: existing approval rules
    approval_rules = group.approval_rules.list()
    assert len(approval_rules) == 1

    new_approval_rule_data = {
        "name": new_approval_rule_name,
        "approvals_required": new_approval_rule_approvals_required,
        "rule_type": "regular",
        "user_ids": new_approval_rule_user_ids,
        "group_ids": group_ids,
    }

    response = group.approval_rules.create(new_approval_rule_data)
    assert response.approvals_required == new_approval_rule_approvals_required
    assert len(response.eligible_approvers) == len(new_approval_rule_user_ids)
    assert response.eligible_approvers[0]["id"] == new_approval_rule_user_ids[0]
    assert response.name == new_approval_rule_name

    # Set the flag to include the new rule in the list response
    list_request_options["include_newly_created_rule"] = True

    # After: list approval rules
    approval_rules = group.approval_rules.list()
    assert len(approval_rules) == 2
    assert approval_rules[1].name == new_approval_rule_name
    assert approval_rules[1].approvals_required == new_approval_rule_approvals_required

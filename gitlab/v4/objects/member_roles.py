"""
GitLab API:
https://docs.gitlab.com/ee/api/instance_level_ci_variables.html
https://docs.gitlab.com/ee/api/project_level_variables.html
https://docs.gitlab.com/ee/api/group_level_variables.html
"""

from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
)
from gitlab.types import RequiredOptional

__all__ = [
    "MemberRole",
    "MemberRoleManager",
    "GroupMemberRole",
    "GroupMemberRoleManager",
]


class MemberRole(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class MemberRoleManager(
    ListMixin[MemberRole], CreateMixin[MemberRole], DeleteMixin[MemberRole]
):
    _path = "/member_roles"
    _obj_cls = MemberRole
    _create_attrs = RequiredOptional(
        required=("name", "base_access_level"),
        optional=(
            "description",
            "admin_cicd_variables",
            "admin_compliance_framework",
            "admin_group_member",
            "admin_group_member",
            "admin_merge_request",
            "admin_push_rules",
            "admin_terraform_state",
            "admin_vulnerability",
            "admin_web_hook",
            "archive_project",
            "manage_deploy_tokens",
            "manage_group_access_tokens",
            "manage_merge_request_settings",
            "manage_project_access_tokens",
            "manage_security_policy_link",
            "read_code",
            "read_runners",
            "read_dependency",
            "read_vulnerability",
            "remove_group",
            "remove_project",
        ),
    )


class GroupMemberRole(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupMemberRoleManager(
    ListMixin[GroupMemberRole],
    CreateMixin[GroupMemberRole],
    DeleteMixin[GroupMemberRole],
):
    _path = "/groups/{group_id}/member_roles"
    _from_parent_attrs = {"group_id": "id"}
    _obj_cls = GroupMemberRole
    _create_attrs = RequiredOptional(
        required=("name", "base_access_level"),
        optional=(
            "description",
            "admin_cicd_variables",
            "admin_compliance_framework",
            "admin_group_member",
            "admin_group_member",
            "admin_merge_request",
            "admin_push_rules",
            "admin_terraform_state",
            "admin_vulnerability",
            "admin_web_hook",
            "archive_project",
            "manage_deploy_tokens",
            "manage_group_access_tokens",
            "manage_merge_request_settings",
            "manage_project_access_tokens",
            "manage_security_policy_link",
            "read_code",
            "read_runners",
            "read_dependency",
            "read_vulnerability",
            "remove_group",
            "remove_project",
        ),
    )

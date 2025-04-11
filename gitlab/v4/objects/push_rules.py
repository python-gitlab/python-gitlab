from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

__all__ = [
    "GroupPushRules",
    "GroupPushRulesManager",
    "ProjectPushRules",
    "ProjectPushRulesManager",
]


class ProjectPushRules(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = None


class ProjectPushRulesManager(
    GetWithoutIdMixin[ProjectPushRules],
    CreateMixin[ProjectPushRules],
    UpdateMixin[ProjectPushRules],
    DeleteMixin[ProjectPushRules],
):
    _path = "/projects/{project_id}/push_rule"
    _obj_cls = ProjectPushRules
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        optional=(
            "author_email_regex",
            "branch_name_regex",
            "commit_committer_check",
            "commit_message_negative_regex",
            "commit_message_regex",
            "deny_delete_tag",
            "file_name_regex",
            "max_file_size",
            "member_check",
            "prevent_secrets",
            "reject_unsigned_commits",
        )
    )
    _update_attrs = RequiredOptional(
        optional=(
            "author_email_regex",
            "branch_name_regex",
            "commit_committer_check",
            "commit_message_negative_regex",
            "commit_message_regex",
            "deny_delete_tag",
            "file_name_regex",
            "max_file_size",
            "member_check",
            "prevent_secrets",
            "reject_unsigned_commits",
        )
    )


class GroupPushRules(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = None


class GroupPushRulesManager(
    GetWithoutIdMixin[GroupPushRules],
    CreateMixin[GroupPushRules],
    UpdateMixin[GroupPushRules],
    DeleteMixin[GroupPushRules],
):
    _path = "/groups/{group_id}/push_rule"
    _obj_cls = GroupPushRules
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        optional=(
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "commit_message_negative_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
            "commit_committer_check",
            "reject_unsigned_commits",
        )
    )
    _update_attrs = RequiredOptional(
        optional=(
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "commit_message_negative_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
            "commit_committer_check",
            "reject_unsigned_commits",
        )
    )

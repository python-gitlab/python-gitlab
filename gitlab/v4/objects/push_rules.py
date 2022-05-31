from typing import Any, cast, Optional, Union

from gitlab.base import RESTManager, RESTObject
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
    "ProjectPushRules",
    "ProjectPushRulesManager",
]


class ProjectPushRules(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = None


class ProjectPushRulesManager(
    GetWithoutIdMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/{project_id}/push_rule"
    _obj_cls = ProjectPushRules
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        optional=(
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
        ),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
        ),
    )

    def get(
        self, id: Optional[Union[int, str]] = None, **kwargs: Any
    ) -> ProjectPushRules:
        return cast(ProjectPushRules, super().get(id=id, **kwargs))

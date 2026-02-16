"""
GitLab API:
https://docs.gitlab.com/api/feature_flag_user_lists
"""

from __future__ import annotations

from gitlab import types
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectFeatureFlagUserList", "ProjectFeatureFlagUserListManager"]


class ProjectFeatureFlagUserList(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "iid"


class ProjectFeatureFlagUserListManager(CRUDMixin[ProjectFeatureFlagUserList]):
    _path = "/projects/{project_id}/feature_flags_user_lists"
    _obj_cls = ProjectFeatureFlagUserList
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("name", "user_xids"))
    _update_attrs = RequiredOptional(optional=("name", "user_xids"))
    _list_filters = ("search",)
    _types = {"user_xids": types.CommaSeparatedStringAttribute}

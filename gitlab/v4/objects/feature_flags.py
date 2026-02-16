"""
GitLab API:
https://docs.gitlab.com/ee/api/feature_flags.html
"""

from __future__ import annotations

from gitlab import types
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectFeatureFlag", "ProjectFeatureFlagManager"]


class ProjectFeatureFlag(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class ProjectFeatureFlagManager(CRUDMixin[ProjectFeatureFlag]):
    _path = "/projects/{project_id}/feature_flags"
    _obj_cls = ProjectFeatureFlag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",), optional=("version", "description", "active", "strategies")
    )
    _update_attrs = RequiredOptional(optional=("description", "active", "strategies"))
    _list_filters = ("scope",)
    _types = {"strategies": types.JsonAttribute}

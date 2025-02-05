from __future__ import annotations

from typing import cast

from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ListMixin,
    ObjectDeleteMixin,
    RefreshMixin,
    SaveMixin,
    UpdateMethod,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

__all__ = ["ProjectJobTokenScope", "ProjectJobTokenScopeManager"]


class ProjectJobTokenScope(RefreshMixin, SaveMixin, RESTObject):
    _id_attr = None

    allowlist: AllowlistProjectManager
    groups_allowlist: AllowlistGroupManager


class ProjectJobTokenScopeManager(
    GetWithoutIdMixin[ProjectJobTokenScope], UpdateMixin[ProjectJobTokenScope]
):
    _path = "/projects/{project_id}/job_token_scope"
    _obj_cls = ProjectJobTokenScope
    _from_parent_attrs = {"project_id": "id"}
    _update_method = UpdateMethod.PATCH


class AllowlistProject(ObjectDeleteMixin, RESTObject):
    _id_attr = "target_project_id"  # note: only true for create endpoint

    def get_id(self) -> int:
        """Returns the id of the resource. This override deals with
        the fact that either an `id` or a `target_project_id` attribute
        is returned by the server depending on the endpoint called."""
        target_project_id = cast(int, super().get_id())
        if target_project_id is not None:
            return target_project_id
        return cast(int, self.id)


class AllowlistProjectManager(
    ListMixin[AllowlistProject],
    CreateMixin[AllowlistProject],
    DeleteMixin[AllowlistProject],
):
    _path = "/projects/{project_id}/job_token_scope/allowlist"
    _obj_cls = AllowlistProject
    _from_parent_attrs = {"project_id": "project_id"}
    _create_attrs = RequiredOptional(required=("target_project_id",))


class AllowlistGroup(ObjectDeleteMixin, RESTObject):
    _id_attr = "target_group_id"  # note: only true for create endpoint

    def get_id(self) -> int:
        """Returns the id of the resource. This override deals with
        the fact that either an `id` or a `target_group_id` attribute
        is returned by the server depending on the endpoint called."""
        target_group_id = cast(int, super().get_id())
        if target_group_id is not None:
            return target_group_id
        return cast(int, self.id)


class AllowlistGroupManager(
    ListMixin[AllowlistGroup], CreateMixin[AllowlistGroup], DeleteMixin[AllowlistGroup]
):
    _path = "/projects/{project_id}/job_token_scope/groups_allowlist"
    _obj_cls = AllowlistGroup
    _from_parent_attrs = {"project_id": "project_id"}
    _create_attrs = RequiredOptional(required=("target_group_id",))

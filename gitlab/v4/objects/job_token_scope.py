from typing import Any, cast

from gitlab.base import RESTManager, RESTObject
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

__all__ = [
    "ProjectJobTokenScope",
    "ProjectJobTokenScopeManager",
]


class ProjectJobTokenScope(RefreshMixin, SaveMixin, RESTObject):
    _id_attr = None

    allowlist: "AllowlistedProjectManager"
    groups_allowlist: "AllowlistedGroupManager"


class ProjectJobTokenScopeManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/projects/{project_id}/job_token_scope"
    _obj_cls = ProjectJobTokenScope
    _from_parent_attrs = {"project_id": "id"}
    _update_method = UpdateMethod.PATCH

    def get(self, **kwargs: Any) -> ProjectJobTokenScope:
        return cast(ProjectJobTokenScope, super().get(**kwargs))


class AllowlistedProject(ObjectDeleteMixin, RESTObject):
    _id_attr = "target_project_id"  # note: only true for create endpoint

    def get_id(self) -> int:
        """Returns the id of the resource. This override deals with
        the fact that either an `id` or a `target_project_id` attribute
        is returned by the server depending on the endpoint called."""
        try:
            return cast(int, getattr(self, self._id_attr))
        except AttributeError:
            return cast(int, getattr(self, "id"))


class AllowlistedProjectManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/{project_id}/job_token_scope/allowlist"
    _obj_cls = AllowlistedProject
    _from_parent_attrs = {"project_id": "project_id"}
    _create_attrs = RequiredOptional(required=("target_project_id",))


class AllowlistedGroup(ObjectDeleteMixin, RESTObject):
    _id_attr = "target_group_id"  # note: only true for create endpoint

    def get_id(self) -> int:
        """Returns the id of the resource. This override deals with
        the fact that either an `id` or a `target_project_id` attribute
        is returned by the server depending on the endpoint called."""
        try:
            return cast(int, getattr(self, self._id_attr))
        except AttributeError:
            return cast(int, getattr(self, "id"))


class AllowlistedGroupManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/{project_id}/job_token_scope/groups_allowlist"
    _obj_cls = AllowlistedProject
    _from_parent_attrs = {"project_id": "project_id"}
    _create_attrs = RequiredOptional(required=("target_group_id",))

from __future__ import annotations

from typing import Any

from gitlab.base import RESTObject, TObjCls
from gitlab.exceptions import GitlabInvitationError
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import ArrayAttribute, CommaSeparatedListAttribute, RequiredOptional

__all__ = [
    "ProjectInvitation",
    "ProjectInvitationManager",
    "GroupInvitation",
    "GroupInvitationManager",
]


class InvitationMixin(CRUDMixin[TObjCls]):
    # pylint: disable=abstract-method
    def create(self, data: dict[str, Any] | None = None, **kwargs: Any) -> TObjCls:
        invitation = super().create(data, **kwargs)

        if invitation.status == "error":
            raise GitlabInvitationError(invitation.message)

        return invitation


class ProjectInvitation(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "email"


class ProjectInvitationManager(InvitationMixin[ProjectInvitation]):
    _path = "/projects/{project_id}/invitations"
    _obj_cls = ProjectInvitation
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("access_level",),
        optional=(
            "expires_at",
            "invite_source",
            "tasks_to_be_done",
            "tasks_project_id",
        ),
        exclusive=("email", "user_id"),
    )
    _update_attrs = RequiredOptional(optional=("access_level", "expires_at"))
    _list_filters = ("query",)
    _types = {
        "email": CommaSeparatedListAttribute,
        "user_id": CommaSeparatedListAttribute,
        "tasks_to_be_done": ArrayAttribute,
    }


class GroupInvitation(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "email"


class GroupInvitationManager(InvitationMixin[GroupInvitation]):
    _path = "/groups/{group_id}/invitations"
    _obj_cls = GroupInvitation
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("access_level",),
        optional=(
            "expires_at",
            "invite_source",
            "tasks_to_be_done",
            "tasks_project_id",
        ),
        exclusive=("email", "user_id"),
    )
    _update_attrs = RequiredOptional(optional=("access_level", "expires_at"))
    _list_filters = ("query",)
    _types = {
        "email": CommaSeparatedListAttribute,
        "user_id": CommaSeparatedListAttribute,
        "tasks_to_be_done": ArrayAttribute,
    }

from __future__ import annotations

from typing import Any

from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ObjectDeleteMixin,
    PromoteMixin,
    RetrieveMixin,
    SaveMixin,
    SubscribableMixin,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

__all__ = ["GroupLabel", "GroupLabelManager", "ProjectLabel", "ProjectLabelManager"]


class GroupLabel(SubscribableMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    manager: GroupLabelManager

    # Update without ID, but we need an ID to get from list.
    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs: Any) -> None:
        """Saves the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct.
            GitlabUpdateError: If the server cannot perform the request.
        """
        updated_data = self._get_updated_data()

        # call the manager
        server_data = self.manager.update(None, updated_data, **kwargs)
        self._update_attrs(server_data)


class GroupLabelManager(
    RetrieveMixin[GroupLabel],
    CreateMixin[GroupLabel],
    UpdateMixin[GroupLabel],
    DeleteMixin[GroupLabel],
):
    _path = "/groups/{group_id}/labels"
    _obj_cls = GroupLabel
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "color"), optional=("description", "priority")
    )
    _update_attrs = RequiredOptional(
        required=("name",), optional=("new_name", "color", "description", "priority")
    )

    # Update without ID.
    # NOTE(jlvillal): Signature doesn't match UpdateMixin.update() so ignore
    # type error
    def update(  # type: ignore[override]
        self, name: str | None, new_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """Update a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        new_data = new_data or {}
        if name:
            new_data["name"] = name
        return super().update(id=None, new_data=new_data, **kwargs)


class ProjectLabel(
    PromoteMixin, SubscribableMixin, SaveMixin, ObjectDeleteMixin, RESTObject
):
    _id_attr = "name"
    manager: ProjectLabelManager

    # Update without ID, but we need an ID to get from list.
    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs: Any) -> None:
        """Saves the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct.
            GitlabUpdateError: If the server cannot perform the request.
        """
        updated_data = self._get_updated_data()

        # call the manager
        server_data = self.manager.update(None, updated_data, **kwargs)
        self._update_attrs(server_data)


class ProjectLabelManager(
    RetrieveMixin[ProjectLabel],
    CreateMixin[ProjectLabel],
    UpdateMixin[ProjectLabel],
    DeleteMixin[ProjectLabel],
):
    _path = "/projects/{project_id}/labels"
    _obj_cls = ProjectLabel
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "color"), optional=("description", "priority")
    )
    _update_attrs = RequiredOptional(
        required=("name",), optional=("new_name", "color", "description", "priority")
    )

    # Update without ID.
    # NOTE(jlvillal): Signature doesn't match UpdateMixin.update() so ignore
    # type error
    def update(  # type: ignore[override]
        self, name: str | None, new_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """Update a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        new_data = new_data or {}
        if name:
            new_data["name"] = name
        return super().update(id=None, new_data=new_data, **kwargs)

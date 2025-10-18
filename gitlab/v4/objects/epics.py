from __future__ import annotations

from typing import Any, TYPE_CHECKING

import gitlab.utils
from gitlab import exceptions as exc
from gitlab import types
from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

from .events import GroupEpicResourceLabelEventManager  # noqa: F401
from .notes import GroupEpicNoteManager  # noqa: F401

__all__ = ["GroupEpic", "GroupEpicManager", "GroupEpicIssue", "GroupEpicIssueManager"]


class GroupEpic(ObjectDeleteMixin, SaveMixin, RESTObject):
    _id_attr = "iid"
    manager: GroupEpicManager

    issues: GroupEpicIssueManager
    resourcelabelevents: GroupEpicResourceLabelEventManager
    notes: GroupEpicNoteManager

    def _epic_path(self) -> str:
        """Return the API path for this epic using its real group."""
        group_id = getattr(self, "group_id", None)
        if group_id is None:
            raise AttributeError(
                "Cannot compute epic path: attribute 'group_id' is missing."
            )
        encoded_group_id = gitlab.utils.EncodedId(group_id)
        return f"/groups/{encoded_group_id}/epics/{self.encoded_id}"

    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs: Any) -> dict[str, Any] | None:
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        This method uses the epic's group_id attribute to construct the correct
        API path. This is important when the epic was retrieved from a parent
        group but actually belongs to a sub-group.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return None

        # Use the epic's actual group_id to construct the correct path.
        path = self._epic_path()

        # Validate and transform the data
        excludes = [self._id_attr] if self._id_attr else []
        self.manager._update_attrs.validate_attrs(data=updated_data, excludes=excludes)

        updated_data, files = gitlab.utils._transform_types(
            data=updated_data, custom_types=self.manager._types, transform_data=False
        )

        # Make the request
        http_method = self.manager._get_update_method()
        server_data = http_method(path, post_data=updated_data, files=files, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)
        return server_data

    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, **kwargs: Any) -> None:
        """Delete the object from the server.

        This method uses the epic's group_id attribute to construct the correct
        API path. This is important when the epic was retrieved from a parent
        group but actually belongs to a sub-group.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        if TYPE_CHECKING:
            assert self.encoded_id is not None

        # Use the epic's actual group_id to construct the correct path.
        path = self._epic_path()
        self.manager.gitlab.http_delete(path, **kwargs)


class GroupEpicManager(CRUDMixin[GroupEpic]):
    _path = "/groups/{group_id}/epics"
    _obj_cls = GroupEpic
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = ("author_id", "labels", "order_by", "sort", "search")
    _create_attrs = RequiredOptional(
        required=("title",),
        optional=("labels", "description", "start_date", "end_date"),
    )
    _update_attrs = RequiredOptional(
        optional=("title", "labels", "description", "start_date", "end_date")
    )
    _types = {"labels": types.CommaSeparatedListAttribute}


class GroupEpicIssue(ObjectDeleteMixin, SaveMixin, RESTObject):
    _id_attr = "epic_issue_id"
    # Define type for 'manager' here So mypy won't complain about
    # 'self.manager.update()' call in the 'save' method.
    manager: GroupEpicIssueManager

    def save(self, **kwargs: Any) -> None:
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return

        # call the manager
        obj_id = self.encoded_id
        self.manager.update(obj_id, updated_data, **kwargs)


class GroupEpicIssueManager(
    ListMixin[GroupEpicIssue],
    CreateMixin[GroupEpicIssue],
    UpdateMixin[GroupEpicIssue],
    DeleteMixin[GroupEpicIssue],
):
    _path = "/groups/{group_id}/epics/{epic_iid}/issues"
    _obj_cls = GroupEpicIssue
    _from_parent_attrs = {"group_id": "group_id", "epic_iid": "iid"}
    _create_attrs = RequiredOptional(required=("issue_id",))
    _update_attrs = RequiredOptional(optional=("move_before_id", "move_after_id"))

    @exc.on_http_error(exc.GitlabCreateError)
    def create(
        self, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> GroupEpicIssue:
        """Create a new object.

        Args:
            data: Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            A new instance of the manage object class build with
                the data sent by the server
        """
        if TYPE_CHECKING:
            assert data is not None
        self._create_attrs.validate_attrs(data=data)
        path = f"{self.path}/{data.pop('issue_id')}"
        server_data = self.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        # The epic_issue_id attribute doesn't exist when creating the resource,
        # but is used everywhere elese. Let's create it to be consistent client
        # side
        server_data["epic_issue_id"] = server_data["id"]
        return self._obj_cls(self, server_data)

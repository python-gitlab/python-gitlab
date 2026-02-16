"""
GitLab API:
https://docs.gitlab.com/ee/api/feature_flags.html
"""

from __future__ import annotations

import json
from typing import Any

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

    def create(
        self, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> ProjectFeatureFlag:
        """Create a new object.

        Args:
            data: Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A new instance of the managed object class build with
                the data sent by the server
        """
        # Handle strategies being passed as a JSON string (e.g. from CLI)
        if "strategies" in kwargs and isinstance(kwargs["strategies"], str):
            kwargs["strategies"] = json.loads(kwargs["strategies"])
        if data and "strategies" in data and isinstance(data["strategies"], str):
            data["strategies"] = json.loads(data["strategies"])

        return super().create(data, **kwargs)

    def update(
        self,
        id: str | int | None = None,
        new_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)
        """
        # Handle strategies being passed as a JSON string (e.g. from CLI)
        if "strategies" in kwargs and isinstance(kwargs["strategies"], str):
            kwargs["strategies"] = json.loads(kwargs["strategies"])
        if (
            new_data
            and "strategies" in new_data
            and isinstance(new_data["strategies"], str)
        ):
            new_data["strategies"] = json.loads(new_data["strategies"])

        return super().update(id, new_data, **kwargs)

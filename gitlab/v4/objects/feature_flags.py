"""
GitLab API:
https://docs.gitlab.com/api/feature_flags
"""

from __future__ import annotations

from typing import Any

from gitlab import types, utils
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectFeatureFlag", "ProjectFeatureFlagManager"]


class ProjectFeatureFlag(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    manager: ProjectFeatureFlagManager

    def _get_save_url_id(self) -> str | int | None:
        """Get the ID used to construct the API URL for the save operation.

        For renames, this must be the *original* name of the flag. For other
        updates, it is the current name.
        """
        if self._id_attr in self._updated_attrs:
            # If the name is being changed, use the original name for the URL.
            obj_id = self._attrs.get(self._id_attr)
            if isinstance(obj_id, str):
                return utils.EncodedId(obj_id)
            return obj_id
        return self.encoded_id

    def save(self, **kwargs: Any) -> dict[str, Any] | None:
        """Save the changes made to the object to the server.

        This is the standard method to use when updating a feature flag object
        that you have already retrieved.

        It is overridden here to correctly handle renaming. When `name` is
        changed, the API requires the *original* name in the URL, and this
        method provides it.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        if not updated_data:
            return None

        obj_id = self._get_save_url_id()
        server_data = self.manager.update(obj_id, updated_data, **kwargs)
        self._update_attrs(server_data)
        return server_data


class ProjectFeatureFlagManager(CRUDMixin[ProjectFeatureFlag]):
    _path = "/projects/{project_id}/feature_flags"
    _obj_cls = ProjectFeatureFlag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",), optional=("version", "description", "active", "strategies")
    )
    _update_attrs = RequiredOptional(
        # new_name is used for renaming via CLI and mapped to 'name' in update()
        optional=("name", "new_name", "description", "active", "strategies")
    )
    _list_filters = ("scope",)
    _types = {"strategies": types.JsonAttribute}

    def update(
        self,
        id: str | int | None = None,
        new_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a Project Feature Flag.

        This is a lower-level method called by `ProjectFeatureFlag.save()` and
        is also used directly by the CLI.

        The `new_name` parameter is a special case to support renaming via the
        CLI (`--new-name`). It is converted to the `name` parameter that the
        GitLab API expects in the request body.

        Args:
            id: The current name of the feature flag.
            new_data: The dictionary of attributes to update.
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        # Avoid mutating the caller-provided new_data dict by working on a copy.
        data = dict(new_data or {})
        # When used via CLI, we have 'new_name' to distinguish from the ID 'name'.
        # When used via .save(), the object passes 'name' directly in new_data.
        if "new_name" in data:
            data["name"] = data.pop("new_name")
        return super().update(id, data, **kwargs)

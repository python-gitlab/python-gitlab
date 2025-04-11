from __future__ import annotations

from typing import Any

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
)
from gitlab.types import RequiredOptional

__all__ = ["DeployKey", "DeployKeyManager", "ProjectKey", "ProjectKeyManager"]


class DeployKey(RESTObject):
    pass


class DeployKeyManager(CreateMixin[DeployKey], ListMixin[DeployKey]):
    _path = "/deploy_keys"
    _obj_cls = DeployKey
    _create_attrs = RequiredOptional(
        required=("title", "key"), optional=("expires_at",)
    )


class ProjectKey(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectKeyManager(CRUDMixin[ProjectKey]):
    _path = "/projects/{project_id}/deploy_keys"
    _obj_cls = ProjectKey
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("title", "key"), optional=("can_push", "expires_at")
    )
    _update_attrs = RequiredOptional(optional=("title", "can_push", "expires_at"))

    @cli.register_custom_action(
        cls_names="ProjectKeyManager",
        required=("key_id",),
        requires_id=False,
        help="Enable a deploy key for the project",
    )
    @exc.on_http_error(exc.GitlabProjectDeployKeyError)
    def enable(self, key_id: int, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Enable a deploy key for a project.

        Args:
            key_id: The ID of the key to enable
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProjectDeployKeyError: If the key could not be enabled

        Returns:
            A dict of the result.
        """
        path = f"{self.path}/{key_id}/enable"
        return self.gitlab.http_post(path, **kwargs)

from gitlab import types
from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
)
from gitlab.types import RequiredOptional

__all__ = [
    "DeployToken",
    "DeployTokenManager",
    "GroupDeployToken",
    "GroupDeployTokenManager",
    "ProjectDeployToken",
    "ProjectDeployTokenManager",
]


class DeployToken(ObjectDeleteMixin, RESTObject):
    pass


class DeployTokenManager(ListMixin[DeployToken]):
    _path = "/deploy_tokens"
    _obj_cls = DeployToken


class GroupDeployToken(ObjectDeleteMixin, RESTObject):
    pass


class GroupDeployTokenManager(
    RetrieveMixin[GroupDeployToken],
    CreateMixin[GroupDeployToken],
    DeleteMixin[GroupDeployToken],
):
    _path = "/groups/{group_id}/deploy_tokens"
    _from_parent_attrs = {"group_id": "id"}
    _obj_cls = GroupDeployToken
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("expires_at", "username")
    )
    _list_filters = ("scopes",)
    _types = {"scopes": types.ArrayAttribute}


class ProjectDeployToken(ObjectDeleteMixin, RESTObject):
    pass


class ProjectDeployTokenManager(
    RetrieveMixin[ProjectDeployToken],
    CreateMixin[ProjectDeployToken],
    DeleteMixin[ProjectDeployToken],
):
    _path = "/projects/{project_id}/deploy_tokens"
    _from_parent_attrs = {"project_id": "id"}
    _obj_cls = ProjectDeployToken
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("expires_at", "username")
    )
    _list_filters = ("scopes",)
    _types = {"scopes": types.ArrayAttribute}

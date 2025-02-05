from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ObjectDeleteMixin,
    ObjectRotateMixin,
    RetrieveMixin,
    RotateMixin,
)
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = ["ProjectAccessToken", "ProjectAccessTokenManager"]


class ProjectAccessToken(ObjectDeleteMixin, ObjectRotateMixin, RESTObject):
    pass


class ProjectAccessTokenManager(
    CreateMixin[ProjectAccessToken],
    DeleteMixin[ProjectAccessToken],
    RetrieveMixin[ProjectAccessToken],
    RotateMixin[ProjectAccessToken],
):
    _path = "/projects/{project_id}/access_tokens"
    _obj_cls = ProjectAccessToken
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("access_level", "expires_at")
    )
    _types = {"scopes": ArrayAttribute}

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "ProjectAccessToken",
    "ProjectAccessTokenManager",
]


class ProjectAccessToken(ObjectDeleteMixin, RESTObject):
    pass


class ProjectAccessTokenManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/{project_id}/access_tokens"
    _obj_cls = ProjectAccessToken
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("access_level", "expires_at")
    )
    _types = {"scopes": ArrayAttribute}

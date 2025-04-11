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

__all__ = ["GroupAccessToken", "GroupAccessTokenManager"]


class GroupAccessToken(ObjectDeleteMixin, ObjectRotateMixin, RESTObject):
    pass


class GroupAccessTokenManager(
    CreateMixin[GroupAccessToken],
    DeleteMixin[GroupAccessToken],
    RetrieveMixin[GroupAccessToken],
    RotateMixin[GroupAccessToken],
):
    _path = "/groups/{group_id}/access_tokens"
    _obj_cls = GroupAccessToken
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("access_level", "expires_at")
    )
    _types = {"scopes": ArrayAttribute}

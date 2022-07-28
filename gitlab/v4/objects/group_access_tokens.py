from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "GroupAccessToken",
    "GroupAccessTokenManager",
]


class GroupAccessToken(ObjectDeleteMixin, RESTObject):
    pass


class GroupAccessTokenManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/groups/{group_id}/access_tokens"
    _obj_cls = GroupAccessToken
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("access_level", "expires_at")
    )
    _types = {"scopes": ArrayAttribute}

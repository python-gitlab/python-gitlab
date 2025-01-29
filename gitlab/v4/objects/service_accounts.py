from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    ObjectRotateMixin,
    RotateMixin,
)
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "ServiceAccount",
    "ServiceAccountManager",
    "GroupServiceAccount",
    "GroupServiceAccountManager",
    "GroupServiceAccountAccessToken",
    "GroupServiceAccountAccessTokenManager",
]


class ServiceAccount(RESTObject):
    pass


class ServiceAccountManager(CreateMixin[ServiceAccount], ListMixin[ServiceAccount]):
    _path = "/service_accounts"
    _obj_cls = ServiceAccount
    _create_attrs = RequiredOptional(optional=("name", "username", "email"))


class GroupServiceAccount(ObjectDeleteMixin, RESTObject):
    pass


class GroupServiceAccountManager(
    CreateMixin[GroupServiceAccount],
    DeleteMixin[GroupServiceAccount],
    ListMixin[GroupServiceAccount],
):
    _path = "/groups/{group_id}/service_accounts"
    _obj_cls = GroupServiceAccount
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(optional=("name", "username"))


class GroupServiceAccountAccessToken(ObjectRotateMixin, RESTObject):
    pass


class GroupServiceAccountAccessTokenManager(
    CreateMixin[GroupServiceAccountAccessToken],
    RotateMixin[GroupServiceAccountAccessToken],
):
    _path = "/groups/{group_id}/service_accounts/{user_id}/personal_access_tokens"
    _obj_cls = GroupServiceAccountAccessToken
    _from_parent_attrs = {"group_id": "id", "user_id": "user_id"}
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("expires_at",)
    )
    _types = {"scopes": ArrayAttribute}

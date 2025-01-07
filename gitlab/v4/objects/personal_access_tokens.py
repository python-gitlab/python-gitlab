from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ObjectDeleteMixin,
    ObjectRotateMixin,
    RetrieveMixin,
    RotateMixin,
)
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "PersonalAccessToken",
    "PersonalAccessTokenManager",
    "UserPersonalAccessToken",
    "UserPersonalAccessTokenManager",
]


class PersonalAccessToken(ObjectDeleteMixin, ObjectRotateMixin, RESTObject):
    pass


class PersonalAccessTokenManager(DeleteMixin, RetrieveMixin, RotateMixin, RESTManager):
    _path = "/personal_access_tokens"
    _obj_cls = PersonalAccessToken
    _list_filters = ("user_id",)


class UserPersonalAccessToken(RESTObject):
    pass


class UserPersonalAccessTokenManager(CreateMixin, RESTManager):
    _path = "/users/{user_id}/personal_access_tokens"
    _obj_cls = UserPersonalAccessToken
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "scopes"), optional=("expires_at",)
    )
    _types = {"scopes": ArrayAttribute}

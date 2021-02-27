from gitlab.base import RESTObject
from gitlab.mixins import ListMixin


__all__ = [
    "PersonalAccessToken",
    "PersonalAccessTokenManager",
]


class PersonalAccessToken(RESTObject):
    pass


class PersonalAccessTokenManager(ListMixin):
    _path = "/personal_access_tokens"
    _obj_cls = PersonalAccessToken
    _list_filters = ("user_id",)

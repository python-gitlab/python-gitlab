from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import ListMixin


__all__ = [
    "PersonalAccessToken",
    "PersonalAccessTokenManager",
]


class PersonalAccessToken(RESTObject):
    pass


class PersonalAccessTokenManager(ListMixin, RESTManager):
    _path = "/personal_access_tokens"
    _obj_cls = PersonalAccessToken
    _list_filters = ("user_id",)

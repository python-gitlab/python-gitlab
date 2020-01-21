from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class CurrentUserEmail(ObjectDeleteMixin, RESTObject):
    _short_print_attr = "email"


class CurrentUserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/user/emails"
    _obj_cls = CurrentUserEmail
    _create_attrs = (("email",), tuple())


class CurrentUserGPGKey(ObjectDeleteMixin, RESTObject):
    pass


class CurrentUserGPGKeyManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/user/gpg_keys"
    _obj_cls = CurrentUserGPGKey
    _create_attrs = (("key",), tuple())


class CurrentUserKey(ObjectDeleteMixin, RESTObject):
    _short_print_attr = "title"


class CurrentUserKeyManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/user/keys"
    _obj_cls = CurrentUserKey
    _create_attrs = (("title", "key"), tuple())


class CurrentUserStatus(SaveMixin, RESTObject):
    _id_attr = None
    _short_print_attr = "message"


class CurrentUserStatusManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/user/status"
    _obj_cls = CurrentUserStatus
    _update_attrs = (tuple(), ("emoji", "message"))


class CurrentUser(RESTObject):
    _id_attr = None
    _short_print_attr = "username"
    _managers = (
        ("status", "CurrentUserStatusManager"),
        ("emails", "CurrentUserEmailManager"),
        ("gpgkeys", "CurrentUserGPGKeyManager"),
        ("keys", "CurrentUserKeyManager"),
    )


class CurrentUserManager(GetWithoutIdMixin, RESTManager):
    _path = "/user"
    _obj_cls = CurrentUser

from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa

__all__ = [
    "Application",
    "ApplicationManager",
]


class Application(ObjectDeleteMixin, RESTObject):
    _url = "/applications"
    _short_print_attr = "name"


class ApplicationManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/applications"
    _obj_cls = Application
    _create_attrs = (("name", "redirect_uri", "scopes"), ("confidential",))

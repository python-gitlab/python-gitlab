from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin
from gitlab.types import ScopesListAttribute

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

    _types = {"scopes": ScopesListAttribute}

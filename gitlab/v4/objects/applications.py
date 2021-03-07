from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin

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
    _create_attrs = RequiredOptional(
        required=("name", "redirect_uri", "scopes"), optional=("confidential",)
    )

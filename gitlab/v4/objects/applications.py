from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin

__all__ = [
    "Application",
    "ApplicationManager",
]


class Application(ObjectDeleteMixin):
    _url = "/applications"
    _short_print_attr = "name"


class ApplicationManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/applications"
    _obj_cls = Application
    _create_attrs = (("name", "redirect_uri", "scopes"), ("confidential",))

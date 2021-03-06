from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import RetrieveMixin


__all__ = [
    "Namespace",
    "NamespaceManager",
]


class Namespace(RESTObject):
    pass


class NamespaceManager(RetrieveMixin, RESTManager):
    _path = "/namespaces"
    _obj_cls = Namespace
    _list_filters = ("search",)

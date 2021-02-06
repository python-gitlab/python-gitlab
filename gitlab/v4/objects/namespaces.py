from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


class Namespace(RESTObject):
    pass


class NamespaceManager(RetrieveMixin, RESTManager):
    _path = "/namespaces"
    _obj_cls = Namespace
    _list_filters = ("search",)

from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class Namespace(RESTObject):
    pass


class NamespaceManager(RetrieveMixin, RESTManager):
    _path = "/namespaces"
    _obj_cls = Namespace
    _list_filters = ("search",)

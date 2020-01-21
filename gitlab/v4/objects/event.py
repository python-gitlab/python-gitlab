from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class Event(RESTObject):
    _id_attr = None
    _short_print_attr = "target_title"


class EventManager(ListMixin, RESTManager):
    _path = "/events"
    _obj_cls = Event
    _list_filters = ("action", "target_type", "before", "after", "sort")

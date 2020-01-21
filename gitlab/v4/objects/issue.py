from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class Issue(RESTObject):
    _url = "/issues"
    _short_print_attr = "title"


class IssueManager(ListMixin, RESTManager):
    _path = "/issues"
    _obj_cls = Issue
    _list_filters = (
        "state",
        "labels",
        "milestone",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "iids",
        "order_by",
        "sort",
        "search",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
    )
    _types = {"labels": types.ListAttribute}

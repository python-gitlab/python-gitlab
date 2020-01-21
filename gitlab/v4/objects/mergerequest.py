from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class MergeRequest(RESTObject):
    pass


class MergeRequestManager(ListMixin, RESTManager):
    _path = "/merge_requests"
    _obj_cls = MergeRequest
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "state",
        "order_by",
        "sort",
        "milestone",
        "view",
        "labels",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
    )
    _types = {"labels": types.ListAttribute}

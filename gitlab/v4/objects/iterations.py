from gitlab import types
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import ListMixin

__all__ = [
    "ProjectIterationManager",
    "GroupIteration",
    "GroupIterationManager",
]


class GroupIteration(RESTObject):
    _repr_attr = "title"


class GroupIterationManager(ListMixin, RESTManager):
    _path = "/groups/{group_id}/iterations"
    _obj_cls = GroupIteration
    _from_parent_attrs = {"group_id": "id"}
    # When using the API, the "in" keyword collides with python's "in" keyword
    # raising a SyntaxError.
    # For this reason, we have to use the query_parameters argument:
    # group.iterations.list(query_parameters={"in": "title"})
    _list_filters = (
        "include_ancestors",
        "include_descendants",
        "in",
        "search",
        "state",
        "updated_after",
        "updated_before",
    )
    _types = {"in": types.ArrayAttribute}


class ProjectIterationManager(ListMixin, RESTManager):
    _path = "/projects/{project_id}/iterations"
    _obj_cls = GroupIteration
    _from_parent_attrs = {"project_id": "id"}
    # When using the API, the "in" keyword collides with python's "in" keyword
    # raising a SyntaxError.
    # For this reason, we have to use the query_parameters argument:
    # project.iterations.list(query_parameters={"in": "title"})
    _list_filters = (
        "include_ancestors",
        "include_descendants",
        "in",
        "search",
        "state",
        "updated_after",
        "updated_before",
    )
    _types = {"in": types.ArrayAttribute}

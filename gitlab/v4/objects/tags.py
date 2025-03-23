from gitlab.base import RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectTag",
    "ProjectTagManager",
    "ProjectProtectedTag",
    "ProjectProtectedTagManager",
]


class ProjectTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _repr_attr = "name"


class ProjectTagManager(NoUpdateMixin[ProjectTag]):
    _path = "/projects/{project_id}/repository/tags"
    _obj_cls = ProjectTag
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("order_by", "sort", "search")
    _create_attrs = RequiredOptional(
        required=("tag_name", "ref"), optional=("message",)
    )


class ProjectProtectedTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _repr_attr = "name"


class ProjectProtectedTagManager(NoUpdateMixin[ProjectProtectedTag]):
    _path = "/projects/{project_id}/protected_tags"
    _obj_cls = ProjectProtectedTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",), optional=("create_access_level",)
    )

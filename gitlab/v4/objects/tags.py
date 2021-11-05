from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin

__all__ = [
    "ProjectTag",
    "ProjectTagManager",
    "ProjectProtectedTag",
    "ProjectProtectedTagManager",
]


class ProjectTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _short_print_attr = "name"


class ProjectTagManager(NoUpdateMixin, RESTManager):
    _path = "/projects/{project_id}/repository/tags"
    _obj_cls = ProjectTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("tag_name", "ref"), optional=("message",)
    )


class ProjectProtectedTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _short_print_attr = "name"


class ProjectProtectedTagManager(NoUpdateMixin, RESTManager):
    _path = "/projects/{project_id}/protected_tags"
    _obj_cls = ProjectProtectedTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",), optional=("create_access_level",)
    )

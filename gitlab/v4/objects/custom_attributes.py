from gitlab.base import RESTObject
from gitlab.mixins import DeleteMixin, ObjectDeleteMixin, RetrieveMixin, SetMixin

__all__ = [
    "GroupCustomAttribute",
    "GroupCustomAttributeManager",
    "ProjectCustomAttribute",
    "ProjectCustomAttributeManager",
    "UserCustomAttribute",
    "UserCustomAttributeManager",
]


class GroupCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class GroupCustomAttributeManager(
    RetrieveMixin[GroupCustomAttribute],
    SetMixin[GroupCustomAttribute],
    DeleteMixin[GroupCustomAttribute],
):
    _path = "/groups/{group_id}/custom_attributes"
    _obj_cls = GroupCustomAttribute
    _from_parent_attrs = {"group_id": "id"}


class ProjectCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectCustomAttributeManager(
    RetrieveMixin[ProjectCustomAttribute],
    SetMixin[ProjectCustomAttribute],
    DeleteMixin[ProjectCustomAttribute],
):
    _path = "/projects/{project_id}/custom_attributes"
    _obj_cls = ProjectCustomAttribute
    _from_parent_attrs = {"project_id": "id"}


class UserCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class UserCustomAttributeManager(
    RetrieveMixin[UserCustomAttribute],
    SetMixin[UserCustomAttribute],
    DeleteMixin[UserCustomAttribute],
):
    _path = "/users/{user_id}/custom_attributes"
    _obj_cls = UserCustomAttribute
    _from_parent_attrs = {"user_id": "id"}

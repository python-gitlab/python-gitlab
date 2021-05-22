from gitlab.base import RESTManager, RESTObject
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


class GroupCustomAttributeManager(RetrieveMixin, SetMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/custom_attributes"
    _obj_cls = GroupCustomAttribute
    _from_parent_attrs = {"group_id": "id"}


class ProjectCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectCustomAttributeManager(RetrieveMixin, SetMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/custom_attributes"
    _obj_cls = ProjectCustomAttribute
    _from_parent_attrs = {"project_id": "id"}


class UserCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class UserCustomAttributeManager(RetrieveMixin, SetMixin, DeleteMixin, RESTManager):
    _path = "/users/%(user_id)s/custom_attributes"
    _obj_cls = UserCustomAttribute
    _from_parent_attrs = {"user_id": "id"}

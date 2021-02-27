from gitlab.base import RESTObject
from gitlab.mixins import DeleteMixin, GetMixin, ListMixin, ObjectDeleteMixin


__all__ = [
    "GroupPackage",
    "GroupPackageManager",
    "ProjectPackage",
    "ProjectPackageManager",
]


class GroupPackage(RESTObject):
    pass


class GroupPackageManager(ListMixin):
    _path = "/groups/%(group_id)s/packages"
    _obj_cls = GroupPackage
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "exclude_subgroups",
        "order_by",
        "sort",
        "package_type",
        "package_name",
    )


class ProjectPackage(ObjectDeleteMixin):
    pass


class ProjectPackageManager(ListMixin, GetMixin, DeleteMixin):
    _path = "/projects/%(project_id)s/packages"
    _obj_cls = ProjectPackage
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "order_by",
        "sort",
        "package_type",
        "package_name",
    )

from gitlab.mixins import (
    AccessRequestMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
)


__all__ = [
    "GroupAccessRequest",
    "GroupAccessRequestManager",
    "ProjectAccessRequest",
    "ProjectAccessRequestManager",
]


class GroupAccessRequest(AccessRequestMixin, ObjectDeleteMixin):
    pass


class GroupAccessRequestManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/groups/%(group_id)s/access_requests"
    _obj_cls = GroupAccessRequest
    _from_parent_attrs = {"group_id": "id"}


class ProjectAccessRequest(AccessRequestMixin, ObjectDeleteMixin):
    pass


class ProjectAccessRequestManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/projects/%(project_id)s/access_requests"
    _obj_cls = ProjectAccessRequest
    _from_parent_attrs = {"project_id": "id"}

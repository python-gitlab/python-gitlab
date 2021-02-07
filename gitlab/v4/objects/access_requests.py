from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "GroupAccessRequest",
    "GroupAccessRequestManager",
    "ProjectAccessRequest",
    "ProjectAccessRequestManager",
]


class GroupAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupAccessRequestManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/access_requests"
    _obj_cls = GroupAccessRequest
    _from_parent_attrs = {"group_id": "id"}


class ProjectAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectAccessRequestManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/access_requests"
    _obj_cls = ProjectAccessRequest
    _from_parent_attrs = {"project_id": "id"}

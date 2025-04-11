from gitlab.base import RESTObject
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


class GroupAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupAccessRequestManager(
    ListMixin[GroupAccessRequest],
    CreateMixin[GroupAccessRequest],
    DeleteMixin[GroupAccessRequest],
):
    _path = "/groups/{group_id}/access_requests"
    _obj_cls = GroupAccessRequest
    _from_parent_attrs = {"group_id": "id"}


class ProjectAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectAccessRequestManager(
    ListMixin[ProjectAccessRequest],
    CreateMixin[ProjectAccessRequest],
    DeleteMixin[ProjectAccessRequest],
):
    _path = "/projects/{project_id}/access_requests"
    _obj_cls = ProjectAccessRequest
    _from_parent_attrs = {"project_id": "id"}

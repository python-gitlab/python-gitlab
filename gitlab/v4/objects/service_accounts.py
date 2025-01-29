from gitlab.base import RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ServiceAccount",
    "ServiceAccountManager",
    "GroupServiceAccount",
    "GroupServiceAccountManager",
]


class ServiceAccount(RESTObject):
    pass


class ServiceAccountManager(CreateMixin, ListMixin, RESTManager):
    _path = "/service_accounts"
    _obj_cls = ServiceAccount
    _create_attrs = RequiredOptional(
        optional=("name", "username", "email"),
    )


class GroupServiceAccount(ObjectDeleteMixin, RESTObject):
    pass


class GroupServiceAccountManager(
    CreateMixin[GroupServiceAccount],
    DeleteMixin[GroupServiceAccount],
    ListMixin[GroupServiceAccount],
):
    _path = "/groups/{group_id}/service_accounts"
    _obj_cls = GroupServiceAccount
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(optional=("name", "username"))

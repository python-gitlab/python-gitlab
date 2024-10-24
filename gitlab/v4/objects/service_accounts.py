from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin
from gitlab.types import RequiredOptional

__all__ = ["GroupServiceAccount", "GroupServiceAccountManager"]


class GroupServiceAccount(ObjectDeleteMixin, RESTObject):
    pass


class GroupServiceAccountManager(CreateMixin, DeleteMixin, ListMixin, RESTManager):
    _path = "/groups/{group_id}/service_accounts"
    _obj_cls = GroupServiceAccount
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        optional=("name", "username"),
    )

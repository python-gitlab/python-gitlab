from gitlab import types
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    CRUDMixin,
    DeleteMixin,
    ListMixin,
    MemberAllMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
)

__all__ = [
    "GroupBillableMember",
    "GroupBillableMemberManager",
    "GroupBillableMemberMembership",
    "GroupBillableMemberMembershipManager",
    "GroupMember",
    "GroupMemberManager",
    "GroupMemberAllManager",
    "ProjectMember",
    "ProjectMemberManager",
    "ProjectMemberAllManager",
]


class GroupMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"


class GroupMemberManager(MemberAllMixin, CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/members"
    _obj_cls = GroupMember
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("access_level", "user_id"), optional=("expires_at",)
    )
    _update_attrs = RequiredOptional(
        required=("access_level",), optional=("expires_at",)
    )
    _types = {"user_ids": types.ListAttribute}


class GroupBillableMember(ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"

    memberships: "GroupBillableMemberMembershipManager"


class GroupBillableMemberManager(ListMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/billable_members"
    _obj_cls = GroupBillableMember
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = ("search", "sort")


class GroupBillableMemberMembership(RESTObject):
    _id_attr = "user_id"


class GroupBillableMemberMembershipManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/billable_members/%(user_id)s/memberships"
    _obj_cls = GroupBillableMemberMembership
    _from_parent_attrs = {"group_id": "group_id", "user_id": "id"}


class GroupMemberAllManager(RetrieveMixin, RESTManager):
    _path = "/groups/%(group_id)s/members/all"
    _obj_cls = GroupMember
    _from_parent_attrs = {"group_id": "id"}


class ProjectMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"


class ProjectMemberManager(MemberAllMixin, CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/members"
    _obj_cls = ProjectMember
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("access_level", "user_id"), optional=("expires_at",)
    )
    _update_attrs = RequiredOptional(
        required=("access_level",), optional=("expires_at",)
    )
    _types = {"user_ids": types.ListAttribute}


class ProjectMemberAllManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/members/all"
    _obj_cls = ProjectMember
    _from_parent_attrs = {"project_id": "id"}

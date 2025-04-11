from gitlab.base import RESTObject
from gitlab.mixins import (
    CRUDMixin,
    NoUpdateMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMethod,
)
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectBranch",
    "ProjectBranchManager",
    "ProjectProtectedBranch",
    "ProjectProtectedBranchManager",
]


class ProjectBranch(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class ProjectBranchManager(NoUpdateMixin[ProjectBranch]):
    _path = "/projects/{project_id}/repository/branches"
    _obj_cls = ProjectBranch
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("branch", "ref"))


class ProjectProtectedBranch(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class ProjectProtectedBranchManager(CRUDMixin[ProjectProtectedBranch]):
    _path = "/projects/{project_id}/protected_branches"
    _obj_cls = ProjectProtectedBranch
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",),
        optional=(
            "push_access_level",
            "merge_access_level",
            "unprotect_access_level",
            "allow_force_push",
            "allowed_to_push",
            "allowed_to_merge",
            "allowed_to_unprotect",
            "code_owner_approval_required",
        ),
    )
    _update_method = UpdateMethod.PATCH


class GroupProtectedBranch(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class GroupProtectedBranchManager(CRUDMixin[GroupProtectedBranch]):
    _path = "/groups/{group_id}/protected_branches"
    _obj_cls = GroupProtectedBranch
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",),
        optional=(
            "push_access_level",
            "merge_access_level",
            "unprotect_access_level",
            "allow_force_push",
            "allowed_to_push",
            "allowed_to_merge",
            "allowed_to_unprotect",
            "code_owner_approval_required",
        ),
    )
    _update_method = UpdateMethod.PATCH

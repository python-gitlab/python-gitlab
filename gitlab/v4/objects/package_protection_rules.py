from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMethod,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectPackageProtectionRule",
    "ProjectPackageProtectionRuleManager",
]


class ProjectPackageProtectionRule(ObjectDeleteMixin, SaveMixin, RESTObject):
    _repr_attr = "package_name_pattern"


class ProjectPackageProtectionRuleManager(
    ListMixin, CreateMixin, DeleteMixin, UpdateMixin, RESTManager
):
    _path = "/projects/{project_id}/packages/protection/rules"
    _obj_cls = ProjectPackageProtectionRule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=(
            "package_name_pattern",
            "package_type",
            "minimum_access_level_for_push",
        ),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "package_name_pattern",
            "package_type",
            "minimum_access_level_for_push",
        ),
    )
    _update_method = UpdateMethod.PATCH

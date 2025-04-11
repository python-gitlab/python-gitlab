from gitlab.base import RESTObject
from gitlab.mixins import CreateMixin, ListMixin, SaveMixin, UpdateMethod, UpdateMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectRegistryRepositoryProtectionRule",
    "ProjectRegistryRepositoryProtectionRuleManager",
]


class ProjectRegistryRepositoryProtectionRule(SaveMixin, RESTObject):
    _repr_attr = "repository_path_pattern"


class ProjectRegistryRepositoryProtectionRuleManager(
    ListMixin[ProjectRegistryRepositoryProtectionRule],
    CreateMixin[ProjectRegistryRepositoryProtectionRule],
    UpdateMixin[ProjectRegistryRepositoryProtectionRule],
):
    _path = "/projects/{project_id}/registry/protection/repository/rules"
    _obj_cls = ProjectRegistryRepositoryProtectionRule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("repository_path_pattern",),
        optional=("minimum_access_level_for_push", "minimum_access_level_for_delete"),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "repository_path_pattern",
            "minimum_access_level_for_push",
            "minimum_access_level_for_delete",
        )
    )
    _update_method = UpdateMethod.PATCH

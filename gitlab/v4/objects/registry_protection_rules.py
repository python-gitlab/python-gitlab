from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, ListMixin, SaveMixin, UpdateMethod, UpdateMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectRegistryProtectionRule",
    "ProjectRegistryProtectionRuleManager",
]


class ProjectRegistryProtectionRule(SaveMixin, RESTObject):
    _repr_attr = "repository_path_pattern"


class ProjectRegistryProtectionRuleManager(
    ListMixin, CreateMixin, UpdateMixin, RESTManager
):
    _path = "/projects/{project_id}/registry/protection/rules"
    _obj_cls = ProjectRegistryProtectionRule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("repository_path_pattern",),
        optional=(
            "minimum_access_level_for_push",
            "minimum_access_level_for_delete",
        ),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "repository_path_pattern",
            "minimum_access_level_for_push",
            "minimum_access_level_for_delete",
        ),
    )
    _update_method = UpdateMethod.PATCH

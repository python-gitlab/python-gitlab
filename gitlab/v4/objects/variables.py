"""
GitLab API:
https://docs.gitlab.com/ee/api/instance_level_ci_variables.html
https://docs.gitlab.com/ee/api/project_level_variables.html
https://docs.gitlab.com/ee/api/group_level_variables.html
"""

from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = [
    "Variable",
    "VariableManager",
    "GroupVariable",
    "GroupVariableManager",
    "ProjectVariable",
    "ProjectVariableManager",
]


class Variable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class VariableManager(CRUDMixin[Variable]):
    _path = "/admin/ci/variables"
    _obj_cls = Variable
    _create_attrs = RequiredOptional(
        required=("key", "value"), optional=("protected", "variable_type", "masked")
    )
    _update_attrs = RequiredOptional(
        required=("key", "value"), optional=("protected", "variable_type", "masked")
    )


class GroupVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class GroupVariableManager(CRUDMixin[GroupVariable]):
    _path = "/groups/{group_id}/variables"
    _obj_cls = GroupVariable
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("key", "value"), optional=("protected", "variable_type", "masked")
    )
    _update_attrs = RequiredOptional(
        required=("key", "value"), optional=("protected", "variable_type", "masked")
    )


class ProjectVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectVariableManager(CRUDMixin[ProjectVariable]):
    _path = "/projects/{project_id}/variables"
    _obj_cls = ProjectVariable
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("key", "value"),
        optional=("protected", "variable_type", "masked", "environment_scope"),
    )
    _update_attrs = RequiredOptional(
        required=("key", "value"),
        optional=("protected", "variable_type", "masked", "environment_scope"),
    )

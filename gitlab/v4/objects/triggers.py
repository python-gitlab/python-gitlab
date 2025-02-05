from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectTrigger", "ProjectTriggerManager"]


class ProjectTrigger(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectTriggerManager(CRUDMixin[ProjectTrigger]):
    _path = "/projects/{project_id}/triggers"
    _obj_cls = ProjectTrigger
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("description",))
    _update_attrs = RequiredOptional(required=("description",))

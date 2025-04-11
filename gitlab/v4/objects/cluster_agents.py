from gitlab.base import RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectClusterAgent", "ProjectClusterAgentManager"]


class ProjectClusterAgent(SaveMixin, ObjectDeleteMixin, RESTObject):
    _repr_attr = "name"


class ProjectClusterAgentManager(NoUpdateMixin[ProjectClusterAgent]):
    _path = "/projects/{project_id}/cluster_agents"
    _obj_cls = ProjectClusterAgent
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("name",))

from gitlab.base import RESTObject
from gitlab.mixins import ListMixin

__all__ = ["ProjectMergeTrain", "ProjectMergeTrainManager"]


class ProjectMergeTrain(RESTObject):
    pass


class ProjectMergeTrainManager(ListMixin[ProjectMergeTrain]):
    _path = "/projects/{project_id}/merge_trains"
    _obj_cls = ProjectMergeTrain
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("scope",)

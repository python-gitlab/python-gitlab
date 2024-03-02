from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import GetMixin, ListMixin, UpdateMethod, UpdateMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectMergeTrain",
    "ProjectMergeTrainManager",
    "ProjectMergeTrainMergeRequest",
    "ProjectMergeTrainMergeRequestManager",
]


class ProjectMergeTrainMergeRequest(RESTObject):
    pass


class ProjectMergeTrainMergeRequestManager(GetMixin, UpdateMixin, RESTManager):
    _path = "/projects/{project_id}/merge_trains/merge_requests"
    _obj_cls = ProjectMergeTrainMergeRequest
    _from_parent_attrs = {"project_id": "project_id"}
    _update_method: UpdateMethod = UpdateMethod.POST

    _update_attrs = RequiredOptional(
        optional=("sha", "squash", "when_pipeline_succeeds"),
    )


class ProjectMergeTrain(RESTObject):
    merge_requests: ProjectMergeTrainMergeRequestManager


class ProjectMergeTrainManager(GetMixin, ListMixin, RESTManager):
    _path = "/projects/{project_id}/merge_trains"
    _obj_cls = ProjectMergeTrain
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("scope",)

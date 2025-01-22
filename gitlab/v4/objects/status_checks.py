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
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "ProjectExternalStatusCheck",
    "ProjectExternalStatusCheckManager",
    "ProjectMergeRequestStatusCheck",
    "ProjectMergeRequestStatusCheckManager",
]


class ProjectExternalStatusCheck(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectExternalStatusCheckManager(
    ListMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/{project_id}/external_status_checks"
    _obj_cls = ProjectExternalStatusCheck
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "external_url"),
        optional=("shared_secret", "protected_branch_ids"),
    )
    _update_attrs = RequiredOptional(
        optional=("name", "external_url", "shared_secret", "protected_branch_ids")
    )
    _types = {"protected_branch_ids": ArrayAttribute}


class ProjectMergeRequestStatusCheck(SaveMixin, RESTObject):
    pass


class ProjectMergeRequestStatusCheckManager(ListMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{merge_request_iid}/status_checks"
    _obj_cls = ProjectMergeRequestStatusCheck
    _from_parent_attrs = {"project_id": "project_id", "merge_request_iid": "iid"}
    _update_attrs = RequiredOptional(
        required=("sha", "external_status_check_id", "status")
    )
    _update_method = UpdateMethod.POST

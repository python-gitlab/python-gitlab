from typing import Any, Dict, Optional

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
    ListMixin[ProjectExternalStatusCheck],
    CreateMixin[ProjectExternalStatusCheck],
    UpdateMixin[ProjectExternalStatusCheck],
    DeleteMixin[ProjectExternalStatusCheck],
    RESTManager[ProjectExternalStatusCheck],
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


class ProjectMergeRequestStatusCheckResponse(SaveMixin, RESTObject):
    pass


class ProjectMergeRequestStatusCheckResponseManager(
    UpdateMixin[ProjectMergeRequestStatusCheckResponse],
    RESTManager[ProjectMergeRequestStatusCheckResponse],
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/status_check_responses"
    _obj_cls = ProjectMergeRequestStatusCheckResponse
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _update_attrs = RequiredOptional(
        required=("sha", "external_status_check_id", "status")
    )
    _update_method = UpdateMethod.POST

    def update(  # type: ignore[override]
        self, new_data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Update a Label on the server.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        return super().update(id=None, new_data=new_data, **kwargs)


class ProjectMergeRequestStatusCheck(RESTObject):
    pass


class ProjectMergeRequestStatusCheckManager(
    ListMixin[ProjectMergeRequestStatusCheck],
    RESTManager[ProjectMergeRequestStatusCheck],
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/status_checks"
    _obj_cls = ProjectMergeRequestStatusCheck
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}

from typing import Any, cast, Union

from ...base import RequiredOptional, RESTManager, RESTObject
from ...mixins import CreateMixin, RetrieveMixin, SaveMixin, UpdateMixin
from .merge_requests import ProjectDeploymentMergeRequestManager  # noqa: F401

__all__ = [
    "ProjectDeployment",
    "ProjectDeploymentManager",
]


class ProjectDeployment(SaveMixin, RESTObject):
    mergerequests: ProjectDeploymentMergeRequestManager


class ProjectDeploymentManager(RetrieveMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/{project_id}/deployments"
    _obj_cls = ProjectDeployment
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "order_by",
        "sort",
        "updated_after",
        "updated_before",
        "environment",
        "status",
    )
    _create_attrs = RequiredOptional(
        required=("sha", "ref", "tag", "status", "environment")
    )

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectDeployment:
        return cast(ProjectDeployment, super().get(id=id, lazy=lazy, **kwargs))

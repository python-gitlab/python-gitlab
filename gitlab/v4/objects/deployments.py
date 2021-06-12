from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, RetrieveMixin, SaveMixin, UpdateMixin

from .merge_requests import ProjectDeploymentMergeRequestManager  # noqa: F401

__all__ = [
    "ProjectDeployment",
    "ProjectDeploymentManager",
]


class ProjectDeployment(SaveMixin, RESTObject):
    mergerequests: ProjectDeploymentMergeRequestManager
    _managers = (("mergerequests", "ProjectDeploymentMergeRequestManager"),)


class ProjectDeploymentManager(RetrieveMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/deployments"
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

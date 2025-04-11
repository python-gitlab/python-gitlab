from __future__ import annotations

from gitlab.base import RESTObject
from gitlab.mixins import ListMixin, RetrieveMixin, SaveMixin, UpdateMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectResourceGroup",
    "ProjectResourceGroupManager",
    "ProjectResourceGroupUpcomingJob",
    "ProjectResourceGroupUpcomingJobManager",
]


class ProjectResourceGroup(SaveMixin, RESTObject):
    _id_attr = "key"

    upcoming_jobs: ProjectResourceGroupUpcomingJobManager


class ProjectResourceGroupManager(
    RetrieveMixin[ProjectResourceGroup], UpdateMixin[ProjectResourceGroup]
):
    _path = "/projects/{project_id}/resource_groups"
    _obj_cls = ProjectResourceGroup
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("order_by", "sort", "include_html_description")
    _update_attrs = RequiredOptional(optional=("process_mode",))


class ProjectResourceGroupUpcomingJob(RESTObject):
    pass


class ProjectResourceGroupUpcomingJobManager(
    ListMixin[ProjectResourceGroupUpcomingJob]
):
    _path = "/projects/{project_id}/resource_groups/{resource_group_key}/upcoming_jobs"
    _obj_cls = ProjectResourceGroupUpcomingJob
    _from_parent_attrs = {"project_id": "project_id", "resource_group_key": "key"}

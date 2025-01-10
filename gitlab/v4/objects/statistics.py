from gitlab.base import RESTObject
from gitlab.mixins import GetWithoutIdMixin, RefreshMixin
from gitlab.types import ArrayAttribute

__all__ = [
    "GroupIssuesStatistics",
    "GroupIssuesStatisticsManager",
    "ProjectAdditionalStatistics",
    "ProjectAdditionalStatisticsManager",
    "IssuesStatistics",
    "IssuesStatisticsManager",
    "ProjectIssuesStatistics",
    "ProjectIssuesStatisticsManager",
    "ApplicationStatistics",
    "ApplicationStatisticsManager",
]


class ProjectAdditionalStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectAdditionalStatisticsManager(
    GetWithoutIdMixin[ProjectAdditionalStatistics]
):
    _path = "/projects/{project_id}/statistics"
    _obj_cls = ProjectAdditionalStatistics
    _from_parent_attrs = {"project_id": "id"}


class IssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class IssuesStatisticsManager(GetWithoutIdMixin[IssuesStatistics]):
    _path = "/issues_statistics"
    _obj_cls = IssuesStatistics
    _list_filters = ("iids",)
    _types = {"iids": ArrayAttribute}


class GroupIssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class GroupIssuesStatisticsManager(GetWithoutIdMixin[GroupIssuesStatistics]):
    _path = "/groups/{group_id}/issues_statistics"
    _obj_cls = GroupIssuesStatistics
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = ("iids",)
    _types = {"iids": ArrayAttribute}


class ProjectIssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectIssuesStatisticsManager(GetWithoutIdMixin[ProjectIssuesStatistics]):
    _path = "/projects/{project_id}/issues_statistics"
    _obj_cls = ProjectIssuesStatistics
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("iids",)
    _types = {"iids": ArrayAttribute}


class ApplicationStatistics(RESTObject):
    _id_attr = None


class ApplicationStatisticsManager(GetWithoutIdMixin[ApplicationStatistics]):
    _path = "/application/statistics"
    _obj_cls = ApplicationStatistics

from typing import Any, cast

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import GetWithoutIdMixin, RefreshMixin

__all__ = [
    "GroupIssuesStatistics",
    "GroupIssuesStatisticsManager",
    "ProjectAdditionalStatistics",
    "ProjectAdditionalStatisticsManager",
    "IssuesStatistics",
    "IssuesStatisticsManager",
    "ProjectIssuesStatistics",
    "ProjectIssuesStatisticsManager",
]


class ProjectAdditionalStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectAdditionalStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/{project_id}/statistics"
    _obj_cls = ProjectAdditionalStatistics
    _from_parent_attrs = {"project_id": "id"}

    def get(self, **kwargs: Any) -> ProjectAdditionalStatistics:
        return cast(ProjectAdditionalStatistics, super().get(**kwargs))


class IssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class IssuesStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/issues_statistics"
    _obj_cls = IssuesStatistics

    def get(self, **kwargs: Any) -> IssuesStatistics:
        return cast(IssuesStatistics, super().get(**kwargs))


class GroupIssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class GroupIssuesStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/groups/{group_id}/issues_statistics"
    _obj_cls = GroupIssuesStatistics
    _from_parent_attrs = {"group_id": "id"}

    def get(self, **kwargs: Any) -> GroupIssuesStatistics:
        return cast(GroupIssuesStatistics, super().get(**kwargs))


class ProjectIssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectIssuesStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/{project_id}/issues_statistics"
    _obj_cls = ProjectIssuesStatistics
    _from_parent_attrs = {"project_id": "id"}

    def get(self, **kwargs: Any) -> ProjectIssuesStatistics:
        return cast(ProjectIssuesStatistics, super().get(**kwargs))

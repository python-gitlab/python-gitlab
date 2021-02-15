from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "ProjectAdditionalStatistics",
    "ProjectAdditionalStatisticsManager",
    "ProjectIssuesStatistics",
    "ProjectIssuesStatisticsManager",
]


class ProjectAdditionalStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectAdditionalStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/%(project_id)s/statistics"
    _obj_cls = ProjectAdditionalStatistics
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectIssuesStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues_statistics"
    _obj_cls = ProjectIssuesStatistics
    _from_parent_attrs = {"project_id": "id"}

from gitlab.mixins import GetWithoutIdMixin, RefreshMixin


__all__ = [
    "ProjectAdditionalStatistics",
    "ProjectAdditionalStatisticsManager",
    "ProjectIssuesStatistics",
    "ProjectIssuesStatisticsManager",
]


class ProjectAdditionalStatistics(RefreshMixin):
    _id_attr = None


class ProjectAdditionalStatisticsManager(GetWithoutIdMixin):
    _path = "/projects/%(project_id)s/statistics"
    _obj_cls = ProjectAdditionalStatistics
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssuesStatistics(RefreshMixin):
    _id_attr = None


class ProjectIssuesStatisticsManager(GetWithoutIdMixin):
    _path = "/projects/%(project_id)s/issues_statistics"
    _obj_cls = ProjectIssuesStatistics
    _from_parent_attrs = {"project_id": "id"}

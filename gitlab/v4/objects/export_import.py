from typing import Any, cast, Optional, Union

from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DownloadMixin, GetWithoutIdMixin, RefreshMixin

__all__ = [
    "GroupExport",
    "GroupExportManager",
    "GroupImport",
    "GroupImportManager",
    "ProjectExport",
    "ProjectExportManager",
    "ProjectImport",
    "ProjectImportManager",
]


class GroupExport(DownloadMixin, RESTObject):
    _id_attr = None


class GroupExportManager(GetWithoutIdMixin, CreateMixin, RESTManager):
    _path = "/groups/{group_id}/export"
    _obj_cls = GroupExport
    _from_parent_attrs = {"group_id": "id"}

    def get(self, id: Optional[Union[int, str]] = None, **kwargs: Any) -> GroupExport:
        return cast(GroupExport, super().get(id=id, **kwargs))


class GroupImport(RESTObject):
    _id_attr = None


class GroupImportManager(GetWithoutIdMixin, RESTManager):
    _path = "/groups/{group_id}/import"
    _obj_cls = GroupImport
    _from_parent_attrs = {"group_id": "id"}

    def get(self, id: Optional[Union[int, str]] = None, **kwargs: Any) -> GroupImport:
        return cast(GroupImport, super().get(id=id, **kwargs))


class ProjectExport(DownloadMixin, RefreshMixin, RESTObject):
    _id_attr = None


class ProjectExportManager(GetWithoutIdMixin, CreateMixin, RESTManager):
    _path = "/projects/{project_id}/export"
    _obj_cls = ProjectExport
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(optional=("description",))

    def get(self, id: Optional[Union[int, str]] = None, **kwargs: Any) -> ProjectExport:
        return cast(ProjectExport, super().get(id=id, **kwargs))


class ProjectImport(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectImportManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/{project_id}/import"
    _obj_cls = ProjectImport
    _from_parent_attrs = {"project_id": "id"}

    def get(self, id: Optional[Union[int, str]] = None, **kwargs: Any) -> ProjectImport:
        return cast(ProjectImport, super().get(id=id, **kwargs))

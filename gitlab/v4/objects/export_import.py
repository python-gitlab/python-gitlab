from gitlab.base import RESTObject
from gitlab.mixins import CreateMixin, DownloadMixin, GetWithoutIdMixin, RefreshMixin
from gitlab.types import RequiredOptional

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


class GroupExportManager(GetWithoutIdMixin[GroupExport], CreateMixin[GroupExport]):
    _path = "/groups/{group_id}/export"
    _obj_cls = GroupExport
    _from_parent_attrs = {"group_id": "id"}


class GroupImport(RESTObject):
    _id_attr = None


class GroupImportManager(GetWithoutIdMixin[GroupImport]):
    _path = "/groups/{group_id}/import"
    _obj_cls = GroupImport
    _from_parent_attrs = {"group_id": "id"}


class ProjectExport(DownloadMixin, RefreshMixin, RESTObject):
    _id_attr = None


class ProjectExportManager(
    GetWithoutIdMixin[ProjectExport], CreateMixin[ProjectExport]
):
    _path = "/projects/{project_id}/export"
    _obj_cls = ProjectExport
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(optional=("description",))


class ProjectImport(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectImportManager(GetWithoutIdMixin[ProjectImport]):
    _path = "/projects/{project_id}/import"
    _obj_cls = ProjectImport
    _from_parent_attrs = {"project_id": "id"}

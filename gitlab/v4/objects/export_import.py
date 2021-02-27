from gitlab.base import RESTObject
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


class GroupExport(DownloadMixin):
    _id_attr = None


class GroupExportManager(GetWithoutIdMixin, CreateMixin):
    _path = "/groups/%(group_id)s/export"
    _obj_cls = GroupExport
    _from_parent_attrs = {"group_id": "id"}


class GroupImport(RESTObject):
    _id_attr = None


class GroupImportManager(GetWithoutIdMixin):
    _path = "/groups/%(group_id)s/import"
    _obj_cls = GroupImport
    _from_parent_attrs = {"group_id": "id"}


class ProjectExport(DownloadMixin, RefreshMixin):
    _id_attr = None


class ProjectExportManager(GetWithoutIdMixin, CreateMixin):
    _path = "/projects/%(project_id)s/export"
    _obj_cls = ProjectExport
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (tuple(), ("description",))


class ProjectImport(RefreshMixin):
    _id_attr = None


class ProjectImportManager(GetWithoutIdMixin):
    _path = "/projects/%(project_id)s/import"
    _obj_cls = ProjectImport
    _from_parent_attrs = {"project_id": "id"}

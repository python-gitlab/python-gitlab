from __future__ import annotations

from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "ProjectRelease",
    "ProjectReleaseManager",
    "ProjectReleaseLink",
    "ProjectReleaseLinkManager",
]


class ProjectRelease(SaveMixin, RESTObject):
    _id_attr = "tag_name"

    links: ProjectReleaseLinkManager


class ProjectReleaseManager(CRUDMixin[ProjectRelease]):
    _path = "/projects/{project_id}/releases"
    _obj_cls = ProjectRelease
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("tag_name",), optional=("name", "description", "ref", "assets")
    )
    _list_filters = ("order_by", "sort", "include_html_description")
    _update_attrs = RequiredOptional(
        optional=("name", "description", "milestones", "released_at")
    )
    _types = {"milestones": ArrayAttribute}


class ProjectReleaseLink(ObjectDeleteMixin, SaveMixin, RESTObject):
    pass


class ProjectReleaseLinkManager(CRUDMixin[ProjectReleaseLink]):
    _path = "/projects/{project_id}/releases/{tag_name}/assets/links"
    _obj_cls = ProjectReleaseLink
    _from_parent_attrs = {"project_id": "project_id", "tag_name": "tag_name"}
    _create_attrs = RequiredOptional(
        required=("name", "url"),
        optional=("filepath", "direct_asset_path", "link_type"),
    )
    _update_attrs = RequiredOptional(
        optional=("name", "url", "filepath", "direct_asset_path", "link_type")
    )

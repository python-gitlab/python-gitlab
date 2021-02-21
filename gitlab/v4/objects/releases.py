from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "ProjectRelease",
    "ProjectReleaseManager",
    "ProjectReleaseLink",
    "ProjectReleaseLinkManager",
]


class ProjectRelease(RESTObject):
    _id_attr = "tag_name"
    _managers = (("links", "ProjectReleaseLinkManager"),)


class ProjectReleaseManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/releases"
    _obj_cls = ProjectRelease
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name", "tag_name", "description"), ("ref", "assets"))


class ProjectReleaseLink(RESTObject, ObjectDeleteMixin, SaveMixin):
    pass


class ProjectReleaseLinkManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/releases/%(tag_name)s/assets/links"
    _obj_cls = ProjectReleaseLink
    _from_parent_attrs = {"project_id": "project_id", "tag_name": "tag_name"}
    _create_attrs = (("name", "url"), ("filepath", "link_type"))
    _update_attrs = ((), ("name", "url", "filepath", "link_type"))

from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin

__all__ = [
    "ProjectRelease",
    "ProjectReleaseManager",
    "ProjectReleaseLink",
    "ProjectReleaseLinkManager",
]


class ProjectRelease(SaveMixin, RESTObject):
    _id_attr = "tag_name"

    links: "ProjectReleaseLinkManager"


class ProjectReleaseManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/releases"
    _obj_cls = ProjectRelease
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("tag_name", "description"), optional=("name", "ref", "assets")
    )
    _update_attrs = RequiredOptional(
        optional=("name", "description", "milestones", "released_at")
    )


class ProjectReleaseLink(ObjectDeleteMixin, SaveMixin, RESTObject):
    pass


class ProjectReleaseLinkManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/releases/%(tag_name)s/assets/links"
    _obj_cls = ProjectReleaseLink
    _from_parent_attrs = {"project_id": "project_id", "tag_name": "tag_name"}
    _create_attrs = RequiredOptional(
        required=("name", "url"), optional=("filepath", "link_type")
    )
    _update_attrs = RequiredOptional(optional=("name", "url", "filepath", "link_type"))

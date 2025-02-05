from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin, UploadMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectWiki", "ProjectWikiManager", "GroupWiki", "GroupWikiManager"]


class ProjectWiki(SaveMixin, ObjectDeleteMixin, UploadMixin, RESTObject):
    _id_attr = "slug"
    _repr_attr = "slug"
    _upload_path = "/projects/{project_id}/wikis/attachments"


class ProjectWikiManager(CRUDMixin[ProjectWiki]):
    _path = "/projects/{project_id}/wikis"
    _obj_cls = ProjectWiki
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("title", "content"), optional=("format",)
    )
    _update_attrs = RequiredOptional(optional=("title", "content", "format"))
    _list_filters = ("with_content",)


class GroupWiki(SaveMixin, ObjectDeleteMixin, UploadMixin, RESTObject):
    _id_attr = "slug"
    _repr_attr = "slug"
    _upload_path = "/groups/{group_id}/wikis/attachments"


class GroupWikiManager(CRUDMixin[GroupWiki]):
    _path = "/groups/{group_id}/wikis"
    _obj_cls = GroupWiki
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("title", "content"), optional=("format",)
    )
    _update_attrs = RequiredOptional(optional=("title", "content", "format"))
    _list_filters = ("with_content",)

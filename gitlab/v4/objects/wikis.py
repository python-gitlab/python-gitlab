from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin


__all__ = [
    "ProjectWiki",
    "ProjectWikiManager",
]


class ProjectWiki(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "slug"
    _short_print_attr = "slug"


class ProjectWikiManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/wikis"
    _obj_cls = ProjectWiki
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("title", "content"), ("format",))
    _update_attrs = (tuple(), ("title", "content", "format"))
    _list_filters = ("with_content",)

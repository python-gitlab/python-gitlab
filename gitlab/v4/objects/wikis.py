from typing import Any, cast, Union

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = [
    "ProjectWiki",
    "ProjectWikiManager",
    "GroupWiki",
    "GroupWikiManager",
]


class ProjectWiki(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "slug"
    _repr_attr = "slug"


class ProjectWikiManager(CRUDMixin, RESTManager):
    _path = "/projects/{project_id}/wikis"
    _obj_cls = ProjectWiki
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("title", "content"), optional=("format",)
    )
    _update_attrs = RequiredOptional(optional=("title", "content", "format"))
    _list_filters = ("with_content",)

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectWiki:
        return cast(ProjectWiki, super().get(id=id, lazy=lazy, **kwargs))


class GroupWiki(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "slug"
    _repr_attr = "slug"


class GroupWikiManager(CRUDMixin, RESTManager):
    _path = "/groups/{group_id}/wikis"
    _obj_cls = GroupWiki
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("title", "content"), optional=("format",)
    )
    _update_attrs = RequiredOptional(optional=("title", "content", "format"))
    _list_filters = ("with_content",)

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> GroupWiki:
        return cast(GroupWiki, super().get(id=id, lazy=lazy, **kwargs))

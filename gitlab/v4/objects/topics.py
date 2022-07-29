from typing import Any, cast, Union

from gitlab import types
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = [
    "Topic",
    "TopicManager",
]


class Topic(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class TopicManager(CRUDMixin, RESTManager):
    _path = "/topics"
    _obj_cls = Topic
    _create_attrs = RequiredOptional(
        # NOTE: The `title` field was added and is required in GitLab 15.0 or
        # newer. But not present before that.
        required=("name",),
        optional=("avatar", "description", "title"),
    )
    _update_attrs = RequiredOptional(optional=("avatar", "description", "name"))
    _types = {"avatar": types.ImageAttribute}

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> Topic:
        return cast(Topic, super().get(id=id, lazy=lazy, **kwargs))

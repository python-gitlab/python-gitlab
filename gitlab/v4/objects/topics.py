from typing import Any, cast, Union

from gitlab import types
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, RetrieveMixin, SaveMixin, UpdateMixin

__all__ = [
    "Topic",
    "TopicManager",
]


class Topic(SaveMixin, RESTObject):
    pass


class TopicManager(CreateMixin, RetrieveMixin, UpdateMixin, RESTManager):
    _path = "/topics"
    _obj_cls = Topic
    _create_attrs = RequiredOptional(
        required=("name",), optional=("avatar", "description")
    )
    _update_attrs = RequiredOptional(optional=("avatar", "description", "name"))
    _types = {"avatar": types.ImageAttribute}

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> Topic:
        return cast(Topic, super().get(id=id, lazy=lazy, **kwargs))

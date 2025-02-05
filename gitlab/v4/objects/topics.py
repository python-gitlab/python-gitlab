from __future__ import annotations

from typing import Any, TYPE_CHECKING

from gitlab import cli
from gitlab import exceptions as exc
from gitlab import types
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["Topic", "TopicManager"]


class Topic(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class TopicManager(CRUDMixin[Topic]):
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

    @cli.register_custom_action(
        cls_names="TopicManager", required=("source_topic_id", "target_topic_id")
    )
    @exc.on_http_error(exc.GitlabMRClosedError)
    def merge(
        self, source_topic_id: int | str, target_topic_id: int | str, **kwargs: Any
    ) -> dict[str, Any]:
        """Merge two topics, assigning all projects to the target topic.

        Args:
            source_topic_id: ID of source project topic
            target_topic_id: ID of target project topic
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTopicMergeError: If the merge failed

        Returns:
            The merged topic data (*not* a RESTObject)
        """
        path = f"{self.path}/merge"
        data = {"source_topic_id": source_topic_id, "target_topic_id": target_topic_id}

        server_data = self.gitlab.http_post(path, post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        return server_data

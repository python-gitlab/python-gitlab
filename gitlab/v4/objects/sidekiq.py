from __future__ import annotations

from typing import Any

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTManager, RESTObject

__all__ = ["SidekiqManager"]


class SidekiqManager(RESTManager[RESTObject]):
    """Manager for the Sidekiq methods.

    This manager doesn't actually manage objects but provides helper function
    for the sidekiq metrics API.
    """

    _path = "/sidekiq"
    _obj_cls = RESTObject

    @cli.register_custom_action(cls_names="SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def queue_metrics(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Return the registered queues information.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            Information about the Sidekiq queues
        """
        return self.gitlab.http_get(f"{self.path}/queue_metrics", **kwargs)

    @cli.register_custom_action(cls_names="SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def process_metrics(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Return the registered sidekiq workers.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            Information about the register Sidekiq worker
        """
        return self.gitlab.http_get(f"{self.path}/process_metrics", **kwargs)

    @cli.register_custom_action(cls_names="SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def job_stats(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Return statistics about the jobs performed.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            Statistics about the Sidekiq jobs performed
        """
        return self.gitlab.http_get(f"{self.path}/job_stats", **kwargs)

    @cli.register_custom_action(cls_names="SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def compound_metrics(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Return all available metrics and statistics.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            All available Sidekiq metrics and statistics
        """
        return self.gitlab.http_get(f"{self.path}/compound_metrics", **kwargs)

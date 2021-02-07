from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "SidekiqManager",
]


class SidekiqManager(RESTManager):
    """Manager for the Sidekiq methods.

    This manager doesn't actually manage objects but provides helper fonction
    for the sidekiq metrics API.
    """

    @cli.register_custom_action("SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def queue_metrics(self, **kwargs):
        """Return the registred queues information.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: Information about the Sidekiq queues
        """
        return self.gitlab.http_get("/sidekiq/queue_metrics", **kwargs)

    @cli.register_custom_action("SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def process_metrics(self, **kwargs):
        """Return the registred sidekiq workers.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: Information about the register Sidekiq worker
        """
        return self.gitlab.http_get("/sidekiq/process_metrics", **kwargs)

    @cli.register_custom_action("SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def job_stats(self, **kwargs):
        """Return statistics about the jobs performed.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: Statistics about the Sidekiq jobs performed
        """
        return self.gitlab.http_get("/sidekiq/job_stats", **kwargs)

    @cli.register_custom_action("SidekiqManager")
    @exc.on_http_error(exc.GitlabGetError)
    def compound_metrics(self, **kwargs):
        """Return all available metrics and statistics.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: All available Sidekiq metrics and statistics
        """
        return self.gitlab.http_get("/sidekiq/compound_metrics", **kwargs)

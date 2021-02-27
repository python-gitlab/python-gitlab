from gitlab import cli, utils
from gitlab import exceptions as exc
from gitlab.mixins import RefreshMixin, RetrieveMixin


__all__ = [
    "ProjectJob",
    "ProjectJobManager",
]


class ProjectJob(RefreshMixin):
    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobCancelError)
    def cancel(self, **kwargs):
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobCancelError: If the job could not be canceled
        """
        path = "%s/%s/cancel" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobRetryError)
    def retry(self, **kwargs):
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobRetryError: If the job could not be retried
        """
        path = "%s/%s/retry" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobPlayError)
    def play(self, **kwargs):
        """Trigger a job explicitly.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobPlayError: If the job could not be triggered
        """
        path = "%s/%s/play" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobEraseError)
    def erase(self, **kwargs):
        """Erase the job (remove job artifacts and trace).

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobEraseError: If the job could not be erased
        """
        path = "%s/%s/erase" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabCreateError)
    def keep_artifacts(self, **kwargs):
        """Prevent artifacts from being deleted when expiration is set.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the request could not be performed
        """
        path = "%s/%s/artifacts/keep" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabCreateError)
    def delete_artifacts(self, **kwargs):
        """Delete artifacts of a job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the request could not be performed
        """
        path = "%s/%s/artifacts" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_delete(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def artifacts(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get the job artifacts.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.
        """
        path = "%s/%s/artifacts" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def artifact(self, path, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get a single artifact file from within the job's artifacts archive.

        Args:
            path (str): Path of the artifact
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.
        """
        path = "%s/%s/artifacts/%s" % (self.manager.path, self.get_id(), path)
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def trace(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get the job trace.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The trace
        """
        path = "%s/%s/trace" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectJobManager(RetrieveMixin):
    _path = "/projects/%(project_id)s/jobs"
    _obj_cls = ProjectJob
    _from_parent_attrs = {"project_id": "id"}

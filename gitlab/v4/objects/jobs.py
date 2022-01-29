import warnings
from typing import Any, Callable, cast, Dict, Optional, TYPE_CHECKING, Union

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab import utils
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import RefreshMixin, RetrieveMixin

from .artifacts import ProjectJobArtifactManager  # noqa: F401

__all__ = [
    "ProjectJob",
    "ProjectJobManager",
]


class ProjectJob(RefreshMixin, RESTObject):
    artifacts: ProjectJobArtifactManager

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobCancelError)
    def cancel(self, **kwargs: Any) -> Dict[str, Any]:
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobCancelError: If the job could not be canceled
        """
        path = f"{self.manager.path}/{self.encoded_id}/cancel"
        result = self.manager.gitlab.http_post(path)
        if TYPE_CHECKING:
            assert isinstance(result, dict)
        return result

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobRetryError)
    def retry(self, **kwargs: Any) -> Dict[str, Any]:
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobRetryError: If the job could not be retried
        """
        path = f"{self.manager.path}/{self.encoded_id}/retry"
        result = self.manager.gitlab.http_post(path)
        if TYPE_CHECKING:
            assert isinstance(result, dict)
        return result

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobPlayError)
    def play(self, **kwargs: Any) -> None:
        """Trigger a job explicitly.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobPlayError: If the job could not be triggered
        """
        path = f"{self.manager.path}/{self.encoded_id}/play"
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobEraseError)
    def erase(self, **kwargs: Any) -> None:
        """Erase the job (remove job artifacts and trace).

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobEraseError: If the job could not be erased
        """
        path = f"{self.manager.path}/{self.encoded_id}/erase"
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabCreateError)
    def keep_artifacts(self, *args: Any, **kwargs: Any) -> None:
        warnings.warn(
            "The job.keep_artifacts() method is deprecated and will be "
            "removed in a future version. Use job.artifacts.keep() instead.",
            DeprecationWarning,
        )
        return self.artifacts.keep(*args, **kwargs)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabCreateError)
    def delete_artifacts(self, *args: Any, **kwargs: Any) -> None:
        warnings.warn(
            "The job.delete_artifacts() method is deprecated and will be "
            "removed in a future version. Use job.artifacts.delete() instead.",
            DeprecationWarning,
        )
        return self.artifacts.delete(*args, **kwargs)

    @cli.register_custom_action("ProjectJob", ("path",))
    @exc.on_http_error(exc.GitlabGetError)
    def artifact(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[bytes]:
        warnings.warn(
            "The job.artifact() method is deprecated and will be "
            "removed in a future version. Use job.artifacts.raw() instead.",
            DeprecationWarning,
        )
        return self.artifacts.raw(*args, **kwargs)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def trace(
        self,
        streamed: bool = False,
        action: Optional[Callable[..., Any]] = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Get the job trace.

        Args:
            streamed: If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action: Callable responsible of dealing with chunk of
                data
            chunk_size: Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            The trace
        """
        path = f"{self.manager.path}/{self.encoded_id}/trace"
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return_value = utils.response_content(result, streamed, action, chunk_size)
        if TYPE_CHECKING:
            assert isinstance(return_value, dict)
        return return_value


class ProjectJobManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/jobs"
    _obj_cls = ProjectJob
    _from_parent_attrs = {"project_id": "id"}

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> ProjectJob:
        return cast(ProjectJob, super().get(id=id, lazy=lazy, **kwargs))

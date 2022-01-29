"""
GitLab API:
https://docs.gitlab.com/ee/api/job_artifacts.html
"""
import warnings
from typing import Any, Callable, Optional, TYPE_CHECKING

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab import utils
from gitlab.base import RESTManager

__all__ = [
    "ProjectArtifactManager",
    "ProjectJobArtifactManager",
]


class ProjectArtifactManager(RESTManager):
    _path = "/projects/{project_id}/artifacts"
    _from_parent_attrs = {"project_id": "id"}

    @cli.register_custom_action(
        "Project", ("ref_name", "job"), ("job_token",), custom_action="artifacts"
    )
    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[bytes]:
        warnings.warn(
            "Calling the Project.artifacts() method on project objects directly "
            "is deprecated and will be removed in python-gitlab 4.0.0. "
            "Please use Project.artifacts.download() instead.\n",
            DeprecationWarning,
        )
        return self.download(
            *args,
            **kwargs,
        )

    @exc.on_http_error(exc.GitlabGetError)
    def download(
        self,
        ref_name: str,
        job: str,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> Optional[bytes]:
        """Get the job artifacts archive from a specific tag or branch.

        Args:
            ref_name: Branch or tag name in repository. HEAD or SHA references
            are not supported.
            job: The name of the job.
            job_token: Job token for multi-project pipeline triggers.
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
            The artifacts if `streamed` is False, None otherwise.
        """
        project_path = self._compute_path("/projects/{project_id}")
        path = f"{project_path}/jobs/artifacts/{ref_name}/download"
        result = self.gitlab.http_get(
            path, job=job, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("ref_name", "artifact_path", "job"))
    @exc.on_http_error(exc.GitlabGetError)
    def raw(
        self,
        ref_name: str,
        artifact_path: str,
        job: str,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> Optional[bytes]:
        """Download a single artifact file from a specific tag or branch from
        within the job's artifacts archive.

        Args:
            ref_name: Branch or tag name in repository. HEAD or SHA references
                are not supported.
            artifact_path: Path to a file inside the artifacts archive.
            job: The name of the job.
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
            The artifact if `streamed` is False, None otherwise.
        """
        project_path = self._compute_path("/projects/{project_id}")
        path = f"{project_path}/jobs/artifacts/{ref_name}/raw/{artifact_path}"
        result = self.gitlab.http_get(
            path, streamed=streamed, raw=True, job=job, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectJobArtifactManager(RESTManager):
    _path = "/projects/{project_id}/jobs/{job_id}/artifacts"
    _from_parent_attrs = {"project_id": "project_id", "job_id": "id"}

    @cli.register_custom_action("ProjectJob", custom_action="artifacts")
    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[bytes]:
        warnings.warn(
            "Calling the job.artifacts() method on job objects directly "
            "is deprecated and will be removed in python-gitlab 4.0.0. "
            "Please use job.artifacts.download() instead.\n",
            DeprecationWarning,
        )
        return self.download(
            *args,
            **kwargs,
        )

    @cli.register_custom_action("JobArtifact")
    @exc.on_http_error(exc.GitlabGetError)
    def download(
        self,
        streamed: bool = False,
        action: Optional[Callable[..., Any]] = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> Optional[bytes]:
        """Get the job artifacts.

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
            The artifacts if `streamed` is False, None otherwise.
        """
        if TYPE_CHECKING:
            assert self.path is not None
        result = self.gitlab.http_get(self.path, streamed=streamed, raw=True, **kwargs)

        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def raw(
        self,
        path: str,
        streamed: bool = False,
        action: Optional[Callable[..., Any]] = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> Optional[bytes]:
        """Get a single artifact file from within the job's artifacts archive.

        Args:
            path: Path of the artifact
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
            The artifacts if `streamed` is False, None otherwise.
        """
        path = f"{self.path}/{path}"
        result = self.gitlab.http_get(path, streamed=streamed, raw=True, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)

    @exc.on_http_error(exc.GitlabCreateError)
    def delete(self, **kwargs: Any) -> None:
        """Delete artifacts of a job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the request could not be performed
        """
        if TYPE_CHECKING:
            assert self.path is not None
        self.gitlab.http_delete(self.path, **kwargs)

    @exc.on_http_error(exc.GitlabCreateError)
    def keep(self, **kwargs: Any) -> None:
        """Prevent artifacts from being deleted when expiration is set.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the request could not be performed
        """
        if TYPE_CHECKING:
            assert self.path is not None
        path = f"{self.path}/keep"
        self.gitlab.http_post(path, **kwargs)

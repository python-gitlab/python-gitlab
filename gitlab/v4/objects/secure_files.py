"""
GitLab API:
https://docs.gitlab.com/ee/api/secure_files.html
"""

from __future__ import annotations

from typing import Any, Callable, Iterator, Literal, overload, TYPE_CHECKING

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab import utils
from gitlab.base import RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin
from gitlab.types import FileAttribute, RequiredOptional

__all__ = ["ProjectSecureFile", "ProjectSecureFileManager"]


class ProjectSecureFile(ObjectDeleteMixin, RESTObject):
    @overload
    def download(
        self,
        streamed: Literal[False] = False,
        action: None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[False] = False,
        **kwargs: Any,
    ) -> bytes: ...

    @overload
    def download(
        self,
        streamed: bool = False,
        action: None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[True] = True,
        **kwargs: Any,
    ) -> Iterator[Any]: ...

    @overload
    def download(
        self,
        streamed: Literal[True] = True,
        action: Callable[[bytes], Any] | None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[False] = False,
        **kwargs: Any,
    ) -> None: ...

    @cli.register_custom_action(cls_names="ProjectSecureFile")
    @exc.on_http_error(exc.GitlabGetError)
    def download(
        self,
        streamed: bool = False,
        action: Callable[[bytes], Any] | None = None,
        chunk_size: int = 1024,
        *,
        iterator: bool = False,
        **kwargs: Any,
    ) -> bytes | Iterator[Any] | None:
        """Download the secure file.

        Args:
            streamed: If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            iterator: If True directly return the underlying response
                iterator
            action: Callable responsible of dealing with chunk of
                data
            chunk_size: Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            The artifacts if `streamed` is False, None otherwise."""
        path = f"{self.manager.path}/{self.id}/download"
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(
            result, streamed, action, chunk_size, iterator=iterator
        )


class ProjectSecureFileManager(NoUpdateMixin[ProjectSecureFile]):
    _path = "/projects/{project_id}/secure_files"
    _obj_cls = ProjectSecureFile
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("name", "file"))
    _types = {"file": FileAttribute}

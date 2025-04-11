from __future__ import annotations

from typing import Any, Callable, Iterator, Literal, overload, TYPE_CHECKING

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab import utils
from gitlab.base import RESTObject, RESTObjectList
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin, UserAgentDetailMixin
from gitlab.types import RequiredOptional

from .award_emojis import ProjectSnippetAwardEmojiManager  # noqa: F401
from .discussions import ProjectSnippetDiscussionManager  # noqa: F401
from .notes import ProjectSnippetNoteManager  # noqa: F401

__all__ = ["Snippet", "SnippetManager", "ProjectSnippet", "ProjectSnippetManager"]


class Snippet(UserAgentDetailMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _repr_attr = "title"

    @overload
    def content(
        self,
        streamed: Literal[False] = False,
        action: None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[False] = False,
        **kwargs: Any,
    ) -> bytes: ...

    @overload
    def content(
        self,
        streamed: bool = False,
        action: None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[True] = True,
        **kwargs: Any,
    ) -> Iterator[Any]: ...

    @overload
    def content(
        self,
        streamed: Literal[True] = True,
        action: Callable[[bytes], Any] | None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[False] = False,
        **kwargs: Any,
    ) -> None: ...

    @cli.register_custom_action(cls_names="Snippet")
    @exc.on_http_error(exc.GitlabGetError)
    def content(
        self,
        streamed: bool = False,
        action: Callable[..., Any] | None = None,
        chunk_size: int = 1024,
        *,
        iterator: bool = False,
        **kwargs: Any,
    ) -> bytes | Iterator[Any] | None:
        """Return the content of a snippet.

        Args:
            streamed: If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            iterator: If True directly return the underlying response
                iterator
            action: Callable responsible of dealing with chunk of
                data
            chunk_size: Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            The snippet content
        """
        path = f"/snippets/{self.encoded_id}/raw"
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(
            result, streamed, action, chunk_size, iterator=iterator
        )


class SnippetManager(CRUDMixin[Snippet]):
    _path = "/snippets"
    _obj_cls = Snippet
    _create_attrs = RequiredOptional(
        required=("title",),
        exclusive=("files", "file_name"),
        optional=("description", "content", "visibility"),
    )
    _update_attrs = RequiredOptional(
        optional=("title", "files", "file_name", "content", "visibility", "description")
    )

    @overload
    def list_public(
        self, *, iterator: Literal[False] = False, **kwargs: Any
    ) -> list[Snippet]: ...

    @overload
    def list_public(
        self, *, iterator: Literal[True] = True, **kwargs: Any
    ) -> RESTObjectList[Snippet]: ...

    @overload
    def list_public(
        self, *, iterator: bool = False, **kwargs: Any
    ) -> RESTObjectList[Snippet] | list[Snippet]: ...

    @cli.register_custom_action(cls_names="SnippetManager")
    def list_public(
        self, *, iterator: bool = False, **kwargs: Any
    ) -> RESTObjectList[Snippet] | list[Snippet]:
        """List all public snippets.

        Args:
            get_all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            iterator: If set to True and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabListError: If the list could not be retrieved

        Returns:
            The list of snippets, or a generator if `iterator` is True
        """
        return self.list(path="/snippets/public", iterator=iterator, **kwargs)

    @overload
    def list_all(
        self, *, iterator: Literal[False] = False, **kwargs: Any
    ) -> list[Snippet]: ...

    @overload
    def list_all(
        self, *, iterator: Literal[True] = True, **kwargs: Any
    ) -> RESTObjectList[Snippet]: ...

    @overload
    def list_all(
        self, *, iterator: bool = False, **kwargs: Any
    ) -> RESTObjectList[Snippet] | list[Snippet]: ...

    @cli.register_custom_action(cls_names="SnippetManager")
    def list_all(
        self, *, iterator: bool = False, **kwargs: Any
    ) -> RESTObjectList[Snippet] | list[Snippet]:
        """List all snippets.

        Args:
            get_all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            iterator: If set to True and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabListError: If the list could not be retrieved

        Returns:
            A generator for the snippets list
        """
        return self.list(path="/snippets/all", iterator=iterator, **kwargs)

    @overload
    def public(
        self,
        *,
        iterator: Literal[False] = False,
        page: int | None = None,
        **kwargs: Any,
    ) -> list[Snippet]: ...

    @overload
    def public(
        self, *, iterator: Literal[True] = True, **kwargs: Any
    ) -> RESTObjectList[Snippet]: ...

    @overload
    def public(
        self, *, iterator: bool = False, **kwargs: Any
    ) -> RESTObjectList[Snippet] | list[Snippet]: ...

    def public(
        self, *, iterator: bool = False, **kwargs: Any
    ) -> RESTObjectList[Snippet] | list[Snippet]:
        """List all public snippets.

        Args:
            get_all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            iterator: If set to True and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabListError: If the list could not be retrieved

        Returns:
            The list of snippets, or a generator if `iterator` is True
        """
        utils.warn(
            message=(
                "Gitlab.snippets.public() is deprecated and will be removed in a "
                "future major version. Use Gitlab.snippets.list_public() instead."
            ),
            category=DeprecationWarning,
        )
        return self.list(path="/snippets/public", iterator=iterator, **kwargs)


class ProjectSnippet(UserAgentDetailMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _url = "/projects/{project_id}/snippets"
    _repr_attr = "title"

    awardemojis: ProjectSnippetAwardEmojiManager
    discussions: ProjectSnippetDiscussionManager
    notes: ProjectSnippetNoteManager

    @overload
    def content(
        self,
        streamed: Literal[False] = False,
        action: None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[False] = False,
        **kwargs: Any,
    ) -> bytes: ...

    @overload
    def content(
        self,
        streamed: bool = False,
        action: None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[True] = True,
        **kwargs: Any,
    ) -> Iterator[Any]: ...

    @overload
    def content(
        self,
        streamed: Literal[True] = True,
        action: Callable[[bytes], Any] | None = None,
        chunk_size: int = 1024,
        *,
        iterator: Literal[False] = False,
        **kwargs: Any,
    ) -> None: ...

    @cli.register_custom_action(cls_names="ProjectSnippet")
    @exc.on_http_error(exc.GitlabGetError)
    def content(
        self,
        streamed: bool = False,
        action: Callable[..., Any] | None = None,
        chunk_size: int = 1024,
        *,
        iterator: bool = False,
        **kwargs: Any,
    ) -> bytes | Iterator[Any] | None:
        """Return the content of a snippet.

        Args:
            streamed: If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            iterator: If True directly return the underlying response
                iterator
            action: Callable responsible of dealing with chunk of
                data
            chunk_size: Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            The snippet content
        """
        path = f"{self.manager.path}/{self.encoded_id}/raw"
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(
            result, streamed, action, chunk_size, iterator=iterator
        )


class ProjectSnippetManager(CRUDMixin[ProjectSnippet]):
    _path = "/projects/{project_id}/snippets"
    _obj_cls = ProjectSnippet
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("title", "visibility"),
        exclusive=("files", "file_name"),
        optional=("description", "content"),
    )
    _update_attrs = RequiredOptional(
        optional=("title", "files", "file_name", "content", "visibility", "description")
    )

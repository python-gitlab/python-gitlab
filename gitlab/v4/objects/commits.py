from __future__ import annotations

from typing import Any, TYPE_CHECKING

import requests

import gitlab
from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import CreateMixin, ListMixin, RefreshMixin, RetrieveMixin
from gitlab.types import RequiredOptional

from .discussions import ProjectCommitDiscussionManager  # noqa: F401

__all__ = [
    "ProjectCommit",
    "ProjectCommitManager",
    "ProjectCommitComment",
    "ProjectCommitCommentManager",
    "ProjectCommitStatus",
    "ProjectCommitStatusManager",
]


class ProjectCommit(RESTObject):
    _repr_attr = "title"

    comments: ProjectCommitCommentManager
    discussions: ProjectCommitDiscussionManager
    statuses: ProjectCommitStatusManager

    @cli.register_custom_action(cls_names="ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def diff(self, **kwargs: Any) -> gitlab.GitlabList | list[dict[str, Any]]:
        """Generate the commit diff.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the diff could not be retrieved

        Returns:
            The changes done in this commit
        """
        path = f"{self.manager.path}/{self.encoded_id}/diff"
        return self.manager.gitlab.http_list(path, **kwargs)

    @cli.register_custom_action(cls_names="ProjectCommit", required=("branch",))
    @exc.on_http_error(exc.GitlabCherryPickError)
    def cherry_pick(
        self, branch: str, **kwargs: Any
    ) -> dict[str, Any] | requests.Response:
        """Cherry-pick a commit into a branch.

        Args:
            branch: Name of target branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCherryPickError: If the cherry-pick could not be performed

        Returns:
            The new commit data (*not* a RESTObject)
        """
        path = f"{self.manager.path}/{self.encoded_id}/cherry_pick"
        post_data = {"branch": branch}
        return self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)

    @cli.register_custom_action(cls_names="ProjectCommit", optional=("type",))
    @exc.on_http_error(exc.GitlabGetError)
    def refs(
        self, type: str = "all", **kwargs: Any
    ) -> gitlab.GitlabList | list[dict[str, Any]]:
        """List the references the commit is pushed to.

        Args:
            type: The scope of references ('branch', 'tag' or 'all')
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the references could not be retrieved

        Returns:
            The references the commit is pushed to.
        """
        path = f"{self.manager.path}/{self.encoded_id}/refs"
        query_data = {"type": type}
        return self.manager.gitlab.http_list(path, query_data=query_data, **kwargs)

    @cli.register_custom_action(cls_names="ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def merge_requests(self, **kwargs: Any) -> gitlab.GitlabList | list[dict[str, Any]]:
        """List the merge requests related to the commit.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the references could not be retrieved

        Returns:
            The merge requests related to the commit.
        """
        path = f"{self.manager.path}/{self.encoded_id}/merge_requests"
        return self.manager.gitlab.http_list(path, **kwargs)

    @cli.register_custom_action(cls_names="ProjectCommit", required=("branch",))
    @exc.on_http_error(exc.GitlabRevertError)
    def revert(self, branch: str, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Revert a commit on a given branch.

        Args:
            branch: Name of target branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabRevertError: If the revert could not be performed

        Returns:
            The new commit data (*not* a RESTObject)
        """
        path = f"{self.manager.path}/{self.encoded_id}/revert"
        post_data = {"branch": branch}
        return self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)

    @cli.register_custom_action(cls_names="ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def sequence(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Get the sequence number of the commit.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the sequence number could not be retrieved

        Returns:
            The commit's sequence number
        """
        path = f"{self.manager.path}/{self.encoded_id}/sequence"
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action(cls_names="ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def signature(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Get the signature of the commit.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the signature could not be retrieved

        Returns:
            The commit's signature data
        """
        path = f"{self.manager.path}/{self.encoded_id}/signature"
        return self.manager.gitlab.http_get(path, **kwargs)


class ProjectCommitManager(RetrieveMixin[ProjectCommit], CreateMixin[ProjectCommit]):
    _path = "/projects/{project_id}/repository/commits"
    _obj_cls = ProjectCommit
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("branch", "commit_message", "actions"),
        optional=("author_email", "author_name"),
    )
    _list_filters = (
        "all",
        "ref_name",
        "since",
        "until",
        "path",
        "with_stats",
        "first_parent",
        "order",
        "trailers",
    )


class ProjectCommitComment(RESTObject):
    _id_attr = None
    _repr_attr = "note"


class ProjectCommitCommentManager(
    ListMixin[ProjectCommitComment], CreateMixin[ProjectCommitComment]
):
    _path = "/projects/{project_id}/repository/commits/{commit_id}/comments"
    _obj_cls = ProjectCommitComment
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = RequiredOptional(
        required=("note",), optional=("path", "line", "line_type")
    )


class ProjectCommitStatus(RefreshMixin, RESTObject):
    pass


class ProjectCommitStatusManager(
    ListMixin[ProjectCommitStatus], CreateMixin[ProjectCommitStatus]
):
    _path = "/projects/{project_id}/repository/commits/{commit_id}/statuses"
    _obj_cls = ProjectCommitStatus
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = RequiredOptional(
        required=("state",),
        optional=("description", "name", "context", "ref", "target_url", "coverage"),
    )

    @exc.on_http_error(exc.GitlabCreateError)
    def create(
        self, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> ProjectCommitStatus:
        """Create a new object.

        Args:
            data: Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            A new instance of the manage object class build with
                the data sent by the server
        """
        # project_id and commit_id are in the data dict when using the CLI, but
        # they are missing when using only the API
        # See #511
        base_path = "/projects/{project_id}/statuses/{commit_id}"
        path: str | None
        if data is not None and "project_id" in data and "commit_id" in data:
            path = base_path.format(**data)
        else:
            path = self._compute_path(base_path)
        if TYPE_CHECKING:
            assert path is not None
        return super().create(data, path=path, **kwargs)

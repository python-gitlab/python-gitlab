from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, ListMixin, RefreshMixin, RetrieveMixin
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
    _short_print_attr = "title"
    _managers = (
        ("comments", "ProjectCommitCommentManager"),
        ("discussions", "ProjectCommitDiscussionManager"),
        ("statuses", "ProjectCommitStatusManager"),
    )

    @cli.register_custom_action("ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def diff(self, **kwargs):
        """Generate the commit diff.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the diff could not be retrieved

        Returns:
            list: The changes done in this commit
        """
        path = "%s/%s/diff" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("ProjectCommit", ("branch",))
    @exc.on_http_error(exc.GitlabCherryPickError)
    def cherry_pick(self, branch, **kwargs):
        """Cherry-pick a commit into a branch.

        Args:
            branch (str): Name of target branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCherryPickError: If the cherry-pick could not be performed
        """
        path = "%s/%s/cherry_pick" % (self.manager.path, self.get_id())
        post_data = {"branch": branch}
        self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)

    @cli.register_custom_action("ProjectCommit", optional=("type",))
    @exc.on_http_error(exc.GitlabGetError)
    def refs(self, type="all", **kwargs):
        """List the references the commit is pushed to.

        Args:
            type (str): The scope of references ('branch', 'tag' or 'all')
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the references could not be retrieved

        Returns:
            list: The references the commit is pushed to.
        """
        path = "%s/%s/refs" % (self.manager.path, self.get_id())
        data = {"type": type}
        return self.manager.gitlab.http_get(path, query_data=data, **kwargs)

    @cli.register_custom_action("ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def merge_requests(self, **kwargs):
        """List the merge requests related to the commit.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the references could not be retrieved

        Returns:
            list: The merge requests related to the commit.
        """
        path = "%s/%s/merge_requests" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("ProjectCommit", ("branch",))
    @exc.on_http_error(exc.GitlabRevertError)
    def revert(self, branch, **kwargs):
        """Revert a commit on a given branch.

        Args:
            branch (str): Name of target branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabRevertError: If the revert could not be performed

        Returns:
            dict: The new commit data (*not* a RESTObject)
        """
        path = "%s/%s/revert" % (self.manager.path, self.get_id())
        post_data = {"branch": branch}
        return self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)

    @cli.register_custom_action("ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def signature(self, **kwargs):
        """Get the signature of the commit.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the signature could not be retrieved

        Returns:
            dict: The commit's signature data
        """
        path = "%s/%s/signature" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)


class ProjectCommitManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits"
    _obj_cls = ProjectCommit
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("branch", "commit_message", "actions"),
        optional=("author_email", "author_name"),
    )


class ProjectCommitComment(RESTObject):
    _id_attr = None
    _short_print_attr = "note"


class ProjectCommitCommentManager(ListMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits/%(commit_id)s" "/comments"
    _obj_cls = ProjectCommitComment
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = RequiredOptional(
        required=("note",), optional=("path", "line", "line_type")
    )


class ProjectCommitStatus(RefreshMixin, RESTObject):
    pass


class ProjectCommitStatusManager(ListMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits/%(commit_id)s" "/statuses"
    _obj_cls = ProjectCommitStatus
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = RequiredOptional(
        required=("state",),
        optional=("description", "name", "context", "ref", "target_url", "coverage"),
    )

    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        # project_id and commit_id are in the data dict when using the CLI, but
        # they are missing when using only the API
        # See #511
        base_path = "/projects/%(project_id)s/statuses/%(commit_id)s"
        if "project_id" in data and "commit_id" in data:
            path = base_path % data
        else:
            path = self._compute_path(base_path)
        return CreateMixin.create(self, data, path=path, **kwargs)

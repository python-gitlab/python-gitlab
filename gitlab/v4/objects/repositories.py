"""
GitLab API: https://docs.gitlab.com/ee/api/repositories.html

Currently this module only contains repository-related methods for projects.
"""

from gitlab import cli, types, utils
from gitlab import exceptions as exc


class RepositoryMixin:
    @cli.register_custom_action("Project", ("submodule", "branch", "commit_sha"))
    @exc.on_http_error(exc.GitlabUpdateError)
    def update_submodule(self, submodule, branch, commit_sha, **kwargs):
        """Update a project submodule

        Args:
            submodule (str): Full path to the submodule
            branch (str): Name of the branch to commit into
            commit_sha (str): Full commit SHA to update the submodule to
            commit_message (str): Commit message. If no message is provided, a default one will be set (optional)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPutError: If the submodule could not be updated
        """

        submodule = submodule.replace("/", "%2F")  # .replace('.', '%2E')
        path = "/projects/%s/repository/submodules/%s" % (self.get_id(), submodule)
        data = {"branch": branch, "commit_sha": commit_sha}
        if "commit_message" in kwargs:
            data["commit_message"] = kwargs["commit_message"]
        return self.manager.gitlab.http_put(path, post_data=data)

    @cli.register_custom_action("Project", tuple(), ("path", "ref", "recursive"))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_tree(self, path="", ref="", recursive=False, **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref (str): Reference to a commit or branch
            recursive (bool): Whether to get the tree recursively
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The representation of the tree
        """
        gl_path = "/projects/%s/repository/tree" % self.get_id()
        query_data = {"recursive": recursive}
        if path:
            query_data["path"] = path
        if ref:
            query_data["ref"] = ref
        return self.manager.gitlab.http_list(gl_path, query_data=query_data, **kwargs)

    @cli.register_custom_action("Project", ("sha",))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_blob(self, sha, **kwargs):
        """Return a file by blob SHA.

        Args:
            sha(str): ID of the blob
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            dict: The blob content and metadata
        """

        path = "/projects/%s/repository/blobs/%s" % (self.get_id(), sha)
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("Project", ("sha",))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_raw_blob(
        self, sha, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
        """Return the raw file contents for a blob.

        Args:
            sha(str): ID of the blob
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The blob content if streamed is False, None otherwise
        """
        path = "/projects/%s/repository/blobs/%s/raw" % (self.get_id(), sha)
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("from_", "to"))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_compare(self, from_, to, **kwargs):
        """Return a diff between two branches/commits.

        Args:
            from_(str): Source branch/SHA
            to(str): Destination branch/SHA
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The diff
        """
        path = "/projects/%s/repository/compare" % self.get_id()
        query_data = {"from": from_, "to": to}
        return self.manager.gitlab.http_get(path, query_data=query_data, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabGetError)
    def repository_contributors(self, **kwargs):
        """Return a list of contributors for the project.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The contributors
        """
        path = "/projects/%s/repository/contributors" % self.get_id()
        return self.manager.gitlab.http_list(path, **kwargs)

    @cli.register_custom_action("Project", tuple(), ("sha",))
    @exc.on_http_error(exc.GitlabListError)
    def repository_archive(
        self, sha=None, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
        """Return a tarball of the repository.

        Args:
            sha (str): ID of the commit (default branch by default)
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            str: The binary data of the archive
        """
        path = "/projects/%s/repository/archive" % self.get_id()
        query_data = {}
        if sha:
            query_data["sha"] = sha
        result = self.manager.gitlab.http_get(
            path, query_data=query_data, raw=True, streamed=streamed, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_merged_branches(self, **kwargs):
        """Delete merged branches.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/repository/merged_branches" % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    @cli.register_custom_action(
        "Project",
        ("version_tag",),
        ("from", "to", "date", "branch", "trailer", "file", "message"),
    )
    @exc.on_http_error(exc.GitlabCreateError)
    def changelog(self, data=None, **kwargs):
        """Create a changelog entry in the repository.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/repository/changelog" % self.get_id()

        # This is here to avoid clashing with the CLI's `--version` flag

        self.manager.gitlab.http_post(path, data=data, **kwargs)

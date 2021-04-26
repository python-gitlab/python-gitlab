import base64
from gitlab import cli, utils
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMixin,
)


__all__ = [
    "ProjectFile",
    "ProjectFileManager",
]


class ProjectFile(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "file_path"
    _short_print_attr = "file_path"

    def decode(self) -> bytes:
        """Returns the decoded content of the file.

        Returns:
            (bytes): the decoded content.
        """
        return base64.b64decode(self.content)

    def save(self, branch, commit_message, **kwargs):
        """Save the changes made to the file to the server.

        The object is updated to match what the server returns.

        Args:
            branch (str): Branch in which the file will be updated
            commit_message (str): Message to send with the commit
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        self.branch = branch
        self.commit_message = commit_message
        self.file_path = self.file_path.replace("/", "%2F")
        super(ProjectFile, self).save(**kwargs)

    def delete(self, branch, commit_message, **kwargs):
        """Delete the file from the server.

        Args:
            branch (str): Branch from which the file will be removed
            commit_message (str): Commit message for the deletion
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        file_path = self.get_id().replace("/", "%2F")
        self.manager.delete(file_path, branch, commit_message, **kwargs)


class ProjectFileManager(GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/files"
    _obj_cls = ProjectFile
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("file_path", "branch", "content", "commit_message"),
        optional=("encoding", "author_email", "author_name"),
    )
    _update_attrs = RequiredOptional(
        required=("file_path", "branch", "content", "commit_message"),
        optional=("encoding", "author_email", "author_name"),
    )

    @cli.register_custom_action("ProjectFileManager", ("file_path", "ref"))
    def get(self, file_path, ref, **kwargs):
        """Retrieve a single file.

        Args:
            file_path (str): Path of the file to retrieve
            ref (str): Name of the branch, tag or commit
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the file could not be retrieved

        Returns:
            object: The generated RESTObject
        """
        return GetMixin.get(self, file_path, ref=ref, **kwargs)

    @cli.register_custom_action(
        "ProjectFileManager",
        ("file_path", "branch", "content", "commit_message"),
        ("encoding", "author_email", "author_name"),
    )
    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the managed object class built with
                the data sent by the server

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """

        self._check_missing_create_attrs(data)
        new_data = data.copy()
        file_path = new_data.pop("file_path").replace("/", "%2F")
        path = "%s/%s" % (self.path, file_path)
        server_data = self.gitlab.http_post(path, post_data=new_data, **kwargs)
        return self._obj_cls(self, server_data)

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(self, file_path, new_data=None, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        data = new_data.copy()
        file_path = file_path.replace("/", "%2F")
        data["file_path"] = file_path
        path = "%s/%s" % (self.path, file_path)
        self._check_missing_update_attrs(data)
        return self.gitlab.http_put(path, post_data=data, **kwargs)

    @cli.register_custom_action(
        "ProjectFileManager", ("file_path", "branch", "commit_message")
    )
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, file_path, branch, commit_message, **kwargs):
        """Delete a file on the server.

        Args:
            file_path (str): Path of the file to remove
            branch (str): Branch from which the file will be removed
            commit_message (str): Commit message for the deletion
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        path = "%s/%s" % (self.path, file_path.replace("/", "%2F"))
        data = {"branch": branch, "commit_message": commit_message}
        self.gitlab.http_delete(path, query_data=data, **kwargs)

    @cli.register_custom_action("ProjectFileManager", ("file_path", "ref"))
    @exc.on_http_error(exc.GitlabGetError)
    def raw(
        self, file_path, ref, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
        """Return the content of a file for a commit.

        Args:
            ref (str): ID of the commit
            filepath (str): Path of the file to return
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the file could not be retrieved

        Returns:
            str: The file content
        """
        file_path = file_path.replace("/", "%2F").replace(".", "%2E")
        path = "%s/%s/raw" % (self.path, file_path)
        query_data = {"ref": ref}
        result = self.gitlab.http_get(
            path, query_data=query_data, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectFileManager", ("file_path", "ref"))
    @exc.on_http_error(exc.GitlabListError)
    def blame(self, file_path, ref, **kwargs):
        """Return the content of a file for a commit.

        Args:
            file_path (str): Path of the file to retrieve
            ref (str): Name of the branch, tag or commit
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError:  If the server failed to perform the request

        Returns:
            list(blame): a list of commits/lines matching the file
        """
        file_path = file_path.replace("/", "%2F").replace(".", "%2E")
        path = "%s/%s/blame" % (self.path, file_path)
        query_data = {"ref": ref}
        return self.gitlab.http_list(path, query_data, **kwargs)

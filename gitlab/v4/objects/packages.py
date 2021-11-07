"""
GitLab API:
https://docs.gitlab.com/ee/api/packages.html
https://docs.gitlab.com/ee/user/packages/generic_packages/
"""

from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING, Union

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab import utils
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import DeleteMixin, GetMixin, ListMixin, ObjectDeleteMixin

__all__ = [
    "GenericPackage",
    "GenericPackageManager",
    "GroupPackage",
    "GroupPackageManager",
    "ProjectPackage",
    "ProjectPackageManager",
    "ProjectPackageFile",
    "ProjectPackageFileManager",
]


class GenericPackage(RESTObject):
    _id_attr = "package_name"


class GenericPackageManager(RESTManager):
    _path = "/projects/%(project_id)s/packages/generic"
    _obj_cls = GenericPackage
    _from_parent_attrs = {"project_id": "id"}

    @cli.register_custom_action(
        "GenericPackageManager",
        ("package_name", "package_version", "file_name", "path"),
    )
    @exc.on_http_error(exc.GitlabUploadError)
    def upload(
        self,
        package_name: str,
        package_version: str,
        file_name: str,
        path: Union[str, Path],
        **kwargs: Any,
    ) -> GenericPackage:
        """Upload a file as a generic package.

        Args:
            package_name (str): The package name. Must follow generic package
                                name regex rules
            package_version (str): The package version. Must follow semantic
                                version regex rules
            file_name (str): The name of the file as uploaded in the registry
            path (str): The path to a local file to upload

        Raises:
            GitlabConnectionError: If the server cannot be reached
            GitlabUploadError: If the file upload fails
            GitlabUploadError: If ``filepath`` cannot be read

        Returns:
            GenericPackage: An object storing the metadata of the uploaded package.

        https://docs.gitlab.com/ee/user/packages/generic_packages/
        """

        try:
            with open(path, "rb") as f:
                file_data = f.read()
        except OSError:
            raise exc.GitlabUploadError(f"Failed to read package file {path}")

        url = f"{self._computed_path}/{package_name}/{package_version}/{file_name}"
        server_data = self.gitlab.http_put(url, post_data=file_data, raw=True, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)

        return self._obj_cls(
            self,
            attrs={
                "package_name": package_name,
                "package_version": package_version,
                "file_name": file_name,
                "path": path,
                "message": server_data["message"],
            },
        )

    @cli.register_custom_action(
        "GenericPackageManager",
        ("package_name", "package_version", "file_name"),
    )
    @exc.on_http_error(exc.GitlabGetError)
    def download(
        self,
        package_name: str,
        package_version: str,
        file_name: str,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> Optional[bytes]:
        """Download a generic package.

        Args:
            package_name (str): The package name.
            package_version (str): The package version.
            file_name (str): The name of the file in the registry
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
            str: The package content if streamed is False, None otherwise
        """
        path = f"{self._computed_path}/{package_name}/{package_version}/{file_name}"
        result = self.gitlab.http_get(path, streamed=streamed, raw=True, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)


class GroupPackage(RESTObject):
    pass


class GroupPackageManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/packages"
    _obj_cls = GroupPackage
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "exclude_subgroups",
        "order_by",
        "sort",
        "package_type",
        "package_name",
    )


class ProjectPackage(ObjectDeleteMixin, RESTObject):
    package_files: "ProjectPackageFileManager"


class ProjectPackageManager(ListMixin, GetMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/packages"
    _obj_cls = ProjectPackage
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "order_by",
        "sort",
        "package_type",
        "package_name",
    )


class ProjectPackageFile(RESTObject):
    pass


class ProjectPackageFileManager(DeleteMixin, ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/packages/%(package_id)s/package_files"
    _obj_cls = ProjectPackageFile
    _from_parent_attrs = {"project_id": "project_id", "package_id": "id"}

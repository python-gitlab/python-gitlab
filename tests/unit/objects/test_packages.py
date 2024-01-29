"""
GitLab API: https://docs.gitlab.com/ce/api/packages.html
"""

import re

import pytest
import responses

from gitlab import exceptions as exc
from gitlab.v4.objects import (
    GenericPackage,
    GroupPackage,
    ProjectPackage,
    ProjectPackageFile,
    ProjectPackagePipeline,
)

package_content = {
    "id": 1,
    "name": "com/mycompany/my-app",
    "version": "1.0-SNAPSHOT",
    "package_type": "maven",
    "_links": {
        "web_path": "/namespace1/project1/-/packages/1",
        "delete_api_path": "/namespace1/project1/-/packages/1",
    },
    "created_at": "2019-11-27T03:37:38.711Z",
    "pipeline": {
        "id": 123,
        "status": "pending",
        "ref": "new-pipeline",
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "web_url": "https://example.com/foo/bar/pipelines/47",
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "user": {
            "name": "Administrator",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        },
    },
    "versions": [
        {
            "id": 2,
            "version": "2.0-SNAPSHOT",
            "created_at": "2020-04-28T04:42:11.573Z",
            "pipeline": {
                "id": 234,
                "status": "pending",
                "ref": "new-pipeline",
                "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                "web_url": "https://example.com/foo/bar/pipelines/58",
                "created_at": "2016-08-11T11:28:34.085Z",
                "updated_at": "2016-08-11T11:32:35.169Z",
                "user": {
                    "name": "Administrator",
                    "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                },
            },
        }
    ],
}

package_file_content = [
    {
        "id": 25,
        "package_id": 1,
        "created_at": "2018-11-07T15:25:52.199Z",
        "file_name": "my-app-1.5-20181107.152550-1.jar",
        "size": 2421,
        "file_md5": "58e6a45a629910c6ff99145a688971ac",
        "file_sha1": "ebd193463d3915d7e22219f52740056dfd26cbfe",
        "pipelines": [
            {
                "id": 123,
                "status": "pending",
                "ref": "new-pipeline",
                "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
                "web_url": "https://example.com/foo/bar/pipelines/47",
                "created_at": "2016-08-11T11:28:34.085Z",
                "updated_at": "2016-08-11T11:32:35.169Z",
                "user": {
                    "name": "Administrator",
                    "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
                },
            }
        ],
    },
    {
        "id": 26,
        "package_id": 1,
        "created_at": "2018-11-07T15:25:56.776Z",
        "file_name": "my-app-1.5-20181107.152550-1.pom",
        "size": 1122,
        "file_md5": "d90f11d851e17c5513586b4a7e98f1b2",
        "file_sha1": "9608d068fe88aff85781811a42f32d97feb440b5",
    },
    {
        "id": 27,
        "package_id": 1,
        "created_at": "2018-11-07T15:26:00.556Z",
        "file_name": "maven-metadata.xml",
        "size": 767,
        "file_md5": "6dfd0cce1203145a927fef5e3a1c650c",
        "file_sha1": "d25932de56052d320a8ac156f745ece73f6a8cd2",
    },
]

package_pipeline_content = [
    {
        "id": 123,
        "iid": 1,
        "project_id": 1,
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "ref": "new-pipeline",
        "status": "failed",
        "source": "push",
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "web_url": "https://example.com/foo/bar/pipelines/47",
        "user": {
            "id": 1,
            "username": "root",
            "name": "Administrator",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
            "web_url": "http://gdk.test:3001/root",
        },
    },
    {
        "id": 234,
        "iid": 2,
        "project_id": 1,
        "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
        "ref": "new-pipeline",
        "status": "failed",
        "source": "push",
        "created_at": "2016-08-11T11:28:34.085Z",
        "updated_at": "2016-08-11T11:32:35.169Z",
        "web_url": "https://example.com/foo/bar/pipelines/58",
        "user": {
            "id": 1,
            "username": "root",
            "name": "Administrator",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon",
            "web_url": "http://gdk.test:3001/root",
        },
    },
]


package_name = "hello-world"
package_version = "v1.0.0"
file_name = "hello.tar.gz"
file_content = "package content"
package_url = f"http://localhost/api/v4/projects/1/packages/generic/{package_name}/{package_version}/{file_name}"


@pytest.fixture
def resp_list_packages():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/(groups|projects)/1/packages"),
            json=[package_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_package():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/packages/1",
            json=package_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_package():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/packages/1",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_delete_package_file():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/packages/1/package_files/1",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_delete_package_file_list():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/projects/1/packages/1/package_files"
            ),
            json=package_file_content,
            content_type="application/json",
            status=200,
        )
        for pkg_file_id in range(25, 28):
            rsps.add(
                method=responses.DELETE,
                url=f"http://localhost/api/v4/projects/1/packages/1/package_files/{pkg_file_id}",
                status=204,
            )
        yield rsps


@pytest.fixture
def resp_list_package_files():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/projects/1/packages/1/package_files"
            ),
            json=package_file_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_package_pipelines():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/projects/1/packages/1/pipelines"),
            json=package_pipeline_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_upload_generic_package(created_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url=package_url,
            json=created_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_download_generic_package(created_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=package_url,
            body=file_content,
            content_type="application/octet-stream",
            status=200,
        )
        yield rsps


def test_list_project_packages(project, resp_list_packages):
    packages = project.packages.list()
    assert isinstance(packages, list)
    assert isinstance(packages[0], ProjectPackage)
    assert packages[0].version == "1.0-SNAPSHOT"


def test_list_group_packages(group, resp_list_packages):
    packages = group.packages.list()
    assert isinstance(packages, list)
    assert isinstance(packages[0], GroupPackage)
    assert packages[0].version == "1.0-SNAPSHOT"


def test_get_project_package(project, resp_get_package):
    package = project.packages.get(1)
    assert isinstance(package, ProjectPackage)
    assert package.version == "1.0-SNAPSHOT"


def test_delete_project_package(project, resp_delete_package):
    package = project.packages.get(1, lazy=True)
    package.delete()


def test_list_project_package_files(project, resp_list_package_files):
    package = project.packages.get(1, lazy=True)
    package_files = package.package_files.list()
    assert isinstance(package_files, list)
    assert isinstance(package_files[0], ProjectPackageFile)
    assert package_files[0].id == 25


def test_delete_project_package_file_from_package_object(
    project, resp_delete_package_file
):
    package = project.packages.get(1, lazy=True)
    package.package_files.delete(1)


def test_delete_project_package_file_from_package_file_object(
    project, resp_delete_package_file_list
):
    package = project.packages.get(1, lazy=True)
    for package_file in package.package_files.list():
        package_file.delete()


def test_list_project_package_pipelines(project, resp_list_package_pipelines):
    package = project.packages.get(1, lazy=True)
    pipelines = package.pipelines.list()
    assert isinstance(pipelines, list)
    assert isinstance(pipelines[0], ProjectPackagePipeline)
    assert pipelines[0].id == 123


def test_upload_generic_package(tmp_path, project, resp_upload_generic_package):
    path = tmp_path / file_name
    path.write_text(file_content, encoding="utf-8")
    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        path=path,
    )

    assert isinstance(package, GenericPackage)


def test_upload_generic_package_nonexistent_path(tmp_path, project):
    with pytest.raises(exc.GitlabUploadError):
        project.generic_packages.upload(
            package_name=package_name,
            package_version=package_version,
            file_name=file_name,
            path="bad",
        )


def test_upload_generic_package_no_file_and_no_data(tmp_path, project):
    path = tmp_path / file_name

    path.write_text(file_content, encoding="utf-8")

    with pytest.raises(exc.GitlabUploadError):
        project.generic_packages.upload(
            package_name=package_name,
            package_version=package_version,
            file_name=file_name,
        )


def test_upload_generic_package_file_and_data(tmp_path, project):
    path = tmp_path / file_name

    path.write_text(file_content, encoding="utf-8")

    with pytest.raises(exc.GitlabUploadError):
        project.generic_packages.upload(
            package_name=package_name,
            package_version=package_version,
            file_name=file_name,
            path=path,
            data=path.read_bytes(),
        )


def test_upload_generic_package_bytes(tmp_path, project, resp_upload_generic_package):
    path = tmp_path / file_name

    path.write_text(file_content, encoding="utf-8")

    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        data=path.read_bytes(),
    )

    assert isinstance(package, GenericPackage)


def test_upload_generic_package_file(tmp_path, project, resp_upload_generic_package):
    path = tmp_path / file_name

    path.write_text(file_content, encoding="utf-8")

    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        data=path.open(mode="rb"),
    )

    assert isinstance(package, GenericPackage)


def test_download_generic_package(project, resp_download_generic_package):
    package = project.generic_packages.download(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
    )

    assert isinstance(package, bytes)

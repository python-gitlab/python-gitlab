"""
GitLab API: https://docs.gitlab.com/ce/api/packages.html
"""
import re

import pytest
import responses

from gitlab.v4.objects import GroupPackage, ProjectPackage, ProjectPackageFile

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
def resp_delete_package(no_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/packages/1",
            json=no_content,
            content_type="application/json",
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

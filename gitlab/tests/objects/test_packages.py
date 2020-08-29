"""
GitLab API: https://docs.gitlab.com/ce/api/packages.html
"""
import re

import pytest
import responses

from gitlab.v4.objects import GroupPackage, ProjectPackage


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

"""
GitLab API: https://docs.gitlab.com/ee/api/secure_files.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectSecureFile

secure_file_content = {
    "id": 1,
    "name": "myfile.jks",
    "checksum": "16630b189ab34b2e3504f4758e1054d2e478deda510b2b08cc0ef38d12e80aac",
    "checksum_algorithm": "sha256",
    "created_at": "2022-02-22T22:22:22.222Z",
    "expires_at": None,
    "metadata": None,
}


@pytest.fixture
def resp_list_secure_files():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/secure_files",
            json=[secure_file_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_secure_file():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/secure_files",
            json=secure_file_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_download_secure_file(binary_content):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/secure_files/1",
            json=secure_file_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/secure_files/1/download",
            body=binary_content,
            content_type="application/octet-stream",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_remove_secure_file():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/secure_files/1",
            status=204,
        )
        yield rsps


def test_list_secure_files(project, resp_list_secure_files):
    secure_files = project.secure_files.list()
    assert len(secure_files) == 1
    assert secure_files[0].id == 1
    assert secure_files[0].name == "myfile.jks"


def test_create_secure_file(project, resp_create_secure_file):
    secure_files = project.secure_files.create({"name": "test", "file": "myfile.jks"})
    assert secure_files.id == 1
    assert secure_files.name == "myfile.jks"


def test_download_secure_file(project, binary_content, resp_download_secure_file):
    secure_file = project.secure_files.get(1)
    secure_content = secure_file.download()
    assert isinstance(secure_file, ProjectSecureFile)
    assert secure_content == binary_content


def test_remove_secure_file(project, resp_remove_secure_file):
    project.secure_files.delete(1)

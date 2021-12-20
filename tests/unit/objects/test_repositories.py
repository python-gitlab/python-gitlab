"""
GitLab API:
https://docs.gitlab.com/ee/api/repositories.html
https://docs.gitlab.com/ee/api/repository_files.html
"""
from urllib.parse import quote

import pytest
import responses

from gitlab.v4.objects import ProjectFile

file_path = "app/models/key.rb"
ref = "main"


@pytest.fixture
def resp_get_repository_file():
    file_response = {
        "file_name": "key.rb",
        "file_path": file_path,
        "size": 1476,
        "encoding": "base64",
        "content": "IyA9PSBTY2hlbWEgSW5mb3...",
        "content_sha256": "4c294617b60715c1d218e61164a3abd4808a4284cbc30e6728a01ad9aada4481",
        "ref": ref,
        "blob_id": "79f7bbd25901e8334750839545a9bd021f0e4c83",
        "commit_id": "d5a3ff139356ce33e37e73add446f16869741b50",
        "last_commit_id": "570e7b2abdd848b95f2f578043fc23bd6f6fd24d",
    }

    encoded_path = quote(file_path, safe="")

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=f"http://localhost/api/v4/projects/1/repository/files/{encoded_path}",
            json=file_response,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_get_repository_file(project, resp_get_repository_file):
    file = project.files.get(file_path, ref=ref)
    assert isinstance(file, ProjectFile)
    assert file.file_path == file_path

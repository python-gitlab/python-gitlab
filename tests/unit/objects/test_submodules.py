"""
GitLab API: https://docs.gitlab.com/ce/api/repository_submodules.html
"""

import pytest
import responses


@pytest.fixture
def resp_update_submodule():
    content = {
        "id": "ed899a2f4b50b4370feeea94676502b42383c746",
        "short_id": "ed899a2f4b5",
        "title": "Message",
        "author_name": "Author",
        "author_email": "author@example.com",
        "committer_name": "Author",
        "committer_email": "author@example.com",
        "created_at": "2018-09-20T09:26:24.000-07:00",
        "message": "Message",
        "parent_ids": ["ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba"],
        "committed_date": "2018-09-20T09:26:24.000-07:00",
        "authored_date": "2018-09-20T09:26:24.000-07:00",
        "status": None,
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/repository/submodules/foo%2Fbar",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_update_submodule(project, resp_update_submodule):
    ret = project.update_submodule(
        submodule="foo/bar",
        branch="main",
        commit_sha="4c3674f66071e30b3311dac9b9ccc90502a72664",
        commit_message="Message",
    )
    assert isinstance(ret, dict)
    assert ret["message"] == "Message"
    assert ret["id"] == "ed899a2f4b50b4370feeea94676502b42383c746"

"""
GitLab API: https://docs.gitlab.com/ee/api/iterations.html
"""

import re

import pytest
import responses

iterations_content = [
    {
        "id": 53,
        "iid": 13,
        "group_id": 5,
        "title": "Iteration II",
        "description": "Ipsum Lorem ipsum",
        "state": 2,
        "created_at": "2020-01-27T05:07:12.573Z",
        "updated_at": "2020-01-27T05:07:12.573Z",
        "due_date": "2020-02-01",
        "start_date": "2020-02-14",
        "web_url": "http://gitlab.example.com/groups/my-group/-/iterations/13",
    }
]


@pytest.fixture
def resp_iterations_list():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/(groups|projects)/1/iterations"),
            json=iterations_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_group_iterations(group, resp_iterations_list):
    iterations = group.iterations.list()
    assert iterations[0].group_id == 5


def test_list_project_iterations(project, resp_iterations_list):
    iterations = project.iterations.list()
    assert iterations[0].group_id == 5

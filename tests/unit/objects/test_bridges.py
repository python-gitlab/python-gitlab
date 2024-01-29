"""
GitLab API: https://docs.gitlab.com/ee/api/jobs.html#list-pipeline-bridges
"""

import pytest
import responses

from gitlab.v4.objects import ProjectPipelineBridge


@pytest.fixture
def resp_list_bridges():
    export_bridges_content = {
        "commit": {
            "author_email": "admin@example.com",
            "author_name": "Administrator",
            "created_at": "2015-12-24T16:51:14.000+01:00",
            "id": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "message": "Test the CI integration.",
            "short_id": "0ff3ae19",
            "title": "Test the CI integration.",
        },
        "allow_failure": False,
        "created_at": "2015-12-24T15:51:21.802Z",
        "started_at": "2015-12-24T17:54:27.722Z",
        "finished_at": "2015-12-24T17:58:27.895Z",
        "duration": 240,
        "id": 7,
        "name": "teaspoon",
        "pipeline": {
            "id": 6,
            "ref": "main",
            "sha": "0ff3ae198f8601a285adcf5c0fff204ee6fba5fd",
            "status": "pending",
            "created_at": "2015-12-24T15:50:16.123Z",
            "updated_at": "2015-12-24T18:00:44.432Z",
            "web_url": "https://example.com/foo/bar/pipelines/6",
        },
        "ref": "main",
        "stage": "test",
        "status": "pending",
        "tag": False,
        "web_url": "https://example.com/foo/bar/-/jobs/7",
        "user": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://gitlab.dev/root",
            "created_at": "2015-12-21T13:14:24.077Z",
            "public_email": "",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": "",
        },
        "downstream_pipeline": {
            "id": 5,
            "sha": "f62a4b2fb89754372a346f24659212eb8da13601",
            "ref": "main",
            "status": "pending",
            "created_at": "2015-12-24T17:54:27.722Z",
            "updated_at": "2015-12-24T17:58:27.896Z",
            "web_url": "https://example.com/diaspora/diaspora-client/pipelines/5",
        },
    }

    export_pipelines_content = [
        {
            "id": 6,
            "status": "pending",
            "ref": "new-pipeline",
            "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
            "web_url": "https://example.com/foo/bar/pipelines/47",
            "created_at": "2016-08-11T11:28:34.085Z",
            "updated_at": "2016-08-11T11:32:35.169Z",
        },
    ]

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/6/bridges",
            json=[export_bridges_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines",
            json=export_pipelines_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_projects_pipelines_bridges(project, resp_list_bridges):
    pipeline = project.pipelines.list()[0]
    bridges = pipeline.bridges.list()

    assert isinstance(bridges, list)
    assert isinstance(bridges[0], ProjectPipelineBridge)
    assert bridges[0].downstream_pipeline["id"] == 5
    assert (
        bridges[0].downstream_pipeline["sha"]
        == "f62a4b2fb89754372a346f24659212eb8da13601"
    )

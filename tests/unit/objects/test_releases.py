"""
GitLab API:
https://docs.gitlab.com/ee/api/releases/index.html
https://docs.gitlab.com/ee/api/releases/links.html
"""

import re

import pytest
import responses

from gitlab.v4.objects import ProjectReleaseLink

tag_name = "v1.0.0"
release_name = "demo-release"
release_description = "my-rel-desc"
released_at = "2019-03-15T08:00:00Z"
link_name = "hello-world"
link_url = "https://gitlab.example.com/group/hello/-/jobs/688/artifacts/raw/bin/hello-darwin-amd64"
direct_url = f"https://gitlab.example.com/group/hello/-/releases/{tag_name}/downloads/hello-world"
new_link_type = "package"
link_content = {
    "id": 2,
    "name": link_name,
    "url": link_url,
    "direct_asset_url": direct_url,
    "external": False,
    "link_type": "other",
}

release_content = {
    "id": 3,
    "tag_name": tag_name,
    "name": release_name,
    "description": release_description,
    "milestones": [],
    "released_at": released_at,
}

release_url = re.compile(rf"http://localhost/api/v4/projects/1/releases/{tag_name}")
links_url = re.compile(
    rf"http://localhost/api/v4/projects/1/releases/{tag_name}/assets/links"
)
link_id_url = re.compile(
    rf"http://localhost/api/v4/projects/1/releases/{tag_name}/assets/links/1"
)


@pytest.fixture
def resp_list_links():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=links_url,
            json=[link_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_link():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=link_id_url,
            json=link_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_link():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=links_url,
            json=link_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_update_link():
    updated_content = dict(link_content)
    updated_content["link_type"] = new_link_type

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url=link_id_url,
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_link():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url=link_id_url,
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_update_release():
    updated_content = dict(release_content)

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url=release_url,
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_release_links(release, resp_list_links):
    links = release.links.list()
    assert isinstance(links, list)
    assert isinstance(links[0], ProjectReleaseLink)
    assert links[0].url == link_url


def test_get_release_link(release, resp_get_link):
    link = release.links.get(1)
    assert isinstance(link, ProjectReleaseLink)
    assert link.url == link_url


def test_create_release_link(release, resp_create_link):
    link = release.links.create({"url": link_url, "name": link_name})
    assert isinstance(link, ProjectReleaseLink)
    assert link.url == link_url


def test_update_release_link(release, resp_update_link):
    link = release.links.get(1, lazy=True)
    link.link_type = new_link_type
    link.save()
    assert link.link_type == new_link_type


def test_delete_release_link(release, resp_delete_link):
    link = release.links.get(1, lazy=True)
    link.delete()


def test_update_release(release, resp_update_release):
    release.name = release_name
    release.description = release_description
    release.save()
    assert release.name == release_name
    assert release.description == release_description

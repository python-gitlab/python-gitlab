"""
GitLab API: https://docs.gitlab.com/ee/api/project_badges.html
GitLab API: https://docs.gitlab.com/ee/api/group_badges.html
"""

import re

import pytest
import responses

from gitlab.v4.objects import GroupBadge, ProjectBadge

link_url = (
    "http://example.com/ci_status.svg?project=example-org/example-project&ref=main"
)
image_url = "https://example.io/my/badge"

rendered_link_url = (
    "http://example.com/ci_status.svg?project=example-org/example-project&ref=main"
)
rendered_image_url = "https://example.io/my/badge"

new_badge = {
    "link_url": link_url,
    "image_url": image_url,
}

badge_content = {
    "name": "Coverage",
    "id": 1,
    "link_url": link_url,
    "image_url": image_url,
    "rendered_link_url": rendered_image_url,
    "rendered_image_url": rendered_image_url,
}

preview_badge_content = {
    "link_url": link_url,
    "image_url": image_url,
    "rendered_link_url": rendered_link_url,
    "rendered_image_url": rendered_image_url,
}


@pytest.fixture()
def resp_get_badge():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/(projects|groups)/1/badges/1"),
            json=badge_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_list_badges():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/(projects|groups)/1/badges"),
            json=[badge_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_create_badge():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=re.compile(r"http://localhost/api/v4/(projects|groups)/1/badges"),
            json=badge_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_update_badge():
    updated_content = dict(badge_content)
    updated_content["link_url"] = "http://link_url"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url=re.compile(r"http://localhost/api/v4/(projects|groups)/1/badges/1"),
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_delete_badge():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url=re.compile(r"http://localhost/api/v4/(projects|groups)/1/badges/1"),
            status=204,
        )
        yield rsps


@pytest.fixture()
def resp_preview_badge():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/(projects|groups)/1/badges/render"
            ),
            json=preview_badge_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_badges(project, resp_list_badges):
    badges = project.badges.list()
    assert isinstance(badges, list)
    assert isinstance(badges[0], ProjectBadge)


def test_list_group_badges(group, resp_list_badges):
    badges = group.badges.list()
    assert isinstance(badges, list)
    assert isinstance(badges[0], GroupBadge)


def test_get_project_badge(project, resp_get_badge):
    badge = project.badges.get(1)
    assert isinstance(badge, ProjectBadge)
    assert badge.name == "Coverage"
    assert badge.id == 1


def test_get_group_badge(group, resp_get_badge):
    badge = group.badges.get(1)
    assert isinstance(badge, GroupBadge)
    assert badge.name == "Coverage"
    assert badge.id == 1


def test_delete_project_badge(project, resp_delete_badge):
    badge = project.badges.get(1, lazy=True)
    badge.delete()


def test_delete_group_badge(group, resp_delete_badge):
    badge = group.badges.get(1, lazy=True)
    badge.delete()


def test_create_project_badge(project, resp_create_badge):
    badge = project.badges.create(new_badge)
    assert isinstance(badge, ProjectBadge)
    assert badge.image_url == image_url


def test_create_group_badge(group, resp_create_badge):
    badge = group.badges.create(new_badge)
    assert isinstance(badge, GroupBadge)
    assert badge.image_url == image_url


def test_preview_project_badge(project, resp_preview_badge):
    output = project.badges.render(
        link_url=link_url,
        image_url=image_url,
    )
    assert isinstance(output, dict)
    assert "rendered_link_url" in output
    assert "rendered_image_url" in output
    assert output["link_url"] == output["rendered_link_url"]
    assert output["image_url"] == output["rendered_image_url"]


def test_preview_group_badge(group, resp_preview_badge):
    output = group.badges.render(
        link_url=link_url,
        image_url=image_url,
    )
    assert isinstance(output, dict)
    assert "rendered_link_url" in output
    assert "rendered_image_url" in output
    assert output["link_url"] == output["rendered_link_url"]
    assert output["image_url"] == output["rendered_image_url"]


def test_update_project_badge(project, resp_update_badge):
    badge = project.badges.get(1, lazy=True)
    badge.link_url = "http://link_url"
    badge.save()
    assert badge.link_url == "http://link_url"


def test_update_group_badge(group, resp_update_badge):
    badge = group.badges.get(1, lazy=True)
    badge.link_url = "http://link_url"
    badge.save()
    assert badge.link_url == "http://link_url"

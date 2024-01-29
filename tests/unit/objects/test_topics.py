"""
GitLab API:
https://docs.gitlab.com/ce/api/topics.html
"""

import pytest
import responses

from gitlab.v4.objects import Topic

name = "GitLab"
topic_title = "topic title"
new_name = "gitlab-test"
topic_content = {
    "id": 1,
    "name": name,
    "title": topic_title,
    "description": "GitLab is an open source end-to-end software development platform.",
    "total_projects_count": 1000,
    "avatar_url": "http://www.gravatar.com/avatar/a0d477b3ea21970ce6ffcbb817b0b435?s=80&d=identicon",
}
topics_url = "http://localhost/api/v4/topics"
topic_url = f"{topics_url}/1"


@pytest.fixture
def resp_list_topics():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=topics_url,
            json=[topic_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_topic():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=topic_url,
            json=topic_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_topic():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=topics_url,
            json=topic_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_update_topic():
    updated_content = dict(topic_content)
    updated_content["name"] = new_name

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url=topic_url,
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_topic():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url=topic_url,
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_merge_topics():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=f"{topics_url}/merge",
            json=topic_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_topics(gl, resp_list_topics):
    topics = gl.topics.list()
    assert isinstance(topics, list)
    assert isinstance(topics[0], Topic)
    assert topics[0].name == name


def test_get_topic(gl, resp_get_topic):
    topic = gl.topics.get(1)
    assert isinstance(topic, Topic)
    assert topic.name == name


def test_create_topic(gl, resp_create_topic):
    topic = gl.topics.create({"name": name, "title": topic_title})
    assert isinstance(topic, Topic)
    assert topic.name == name
    assert topic.title == topic_title


def test_update_topic(gl, resp_update_topic):
    topic = gl.topics.get(1, lazy=True)
    topic.name = new_name
    topic.save()
    assert topic.name == new_name


def test_delete_topic(gl, resp_delete_topic):
    topic = gl.topics.get(1, lazy=True)
    topic.delete()


def test_merge_topic(gl, resp_merge_topics):
    topic = gl.topics.merge(123, 1)
    assert topic["id"] == 1

"""
GitLab API:
https://docs.gitlab.com/ce/api/topics.html
"""


def test_topics(gl):
    assert not gl.topics.list()

    topic = gl.topics.create({"name": "my-topic", "description": "My Topic"})
    assert topic.name == "my-topic"
    assert gl.topics.list()

    topic.description = "My Updated Topic"
    topic.save()

    updated_topic = gl.topics.get(topic.id)
    assert updated_topic.description == topic.description

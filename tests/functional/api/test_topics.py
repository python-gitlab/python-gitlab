"""
GitLab API:
https://docs.gitlab.com/ce/api/topics.html
"""


def test_topics(gl, gitlab_version):
    assert not gl.topics.list()

    create_dict = {"name": "my-topic", "description": "My Topic"}
    if gitlab_version.major >= 15:
        create_dict["title"] = "my topic title"
    topic = gl.topics.create(create_dict)
    assert topic.name == "my-topic"

    if gitlab_version.major >= 15:
        assert topic.title == "my topic title"

    assert gl.topics.list()

    topic.description = "My Updated Topic"
    topic.save()
    updated_topic = gl.topics.get(topic.id)
    assert updated_topic.description == topic.description

    create_dict = {"name": "my-second-topic", "description": "My Second Topic"}
    if gitlab_version.major >= 15:
        create_dict["title"] = "my second topic title"
    topic2 = gl.topics.create(create_dict)
    merged_topic = gl.topics.merge(topic.id, topic2.id)
    assert merged_topic["id"] == topic2.id

    topic2.delete()

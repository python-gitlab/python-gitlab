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


def test_topic_avatar_upload(gl, fixture_dir):
    """Test uploading an avatar to a topic."""

    topic = gl.topics.create(
        {
            "name": "avatar-topic",
            "description": "Topic with avatar",
            "title": "Avatar Topic",
        }
    )

    with open(fixture_dir / "avatar.png", "rb") as avatar_file:
        topic.avatar = avatar_file
        topic.save()

    updated_topic = gl.topics.get(topic.id)
    assert updated_topic.avatar_url is not None

    topic.delete()


def test_topic_avatar_remove(gl, fixture_dir):
    """Test removing an avatar from a topic."""

    topic = gl.topics.create(
        {
            "name": "avatar-topic-remove",
            "description": "Remove avatar",
            "title": "Remove Avatar",
        }
    )

    with open(fixture_dir / "avatar.png", "rb") as avatar_file:
        topic.avatar = avatar_file
        topic.save()

    topic.avatar = ""
    topic.save()

    updated_topic = gl.topics.get(topic.id)
    assert updated_topic.avatar_url is None

    topic.delete()

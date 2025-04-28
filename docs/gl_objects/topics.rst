########
Topics
########

Topics can be used to categorize projects and find similar new projects. 

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Topic`
  + :class:`gitlab.v4.objects.TopicManager`
  + :attr:`gitlab.Gitlab.topics`

* GitLab API: https://docs.gitlab.com/api/topics

This endpoint requires admin access for creating, updating and deleting objects.

Examples
--------

List project topics on the GitLab instance::

    topics = gl.topics.list(get_all=True)

Get a specific topic by its ID::

    topic = gl.topics.get(topic_id)

Create a new topic::

    topic = gl.topics.create({"name": "my-topic", "title": "my title"})

Update a topic::

    topic.description = "My new topic"
    topic.save()

    # or
    gl.topics.update(topic_id, {"description": "My new topic"})

Delete a topic::

    topic.delete()

    # or
    gl.topics.delete(topic_id)

Merge a source topic into a target topic::

    gl.topics.merge(topic_id, target_topic_id)

Set the avatar image for a topic::

    # the avatar image can be passed as data (content of the file) or as a file
    # object opened in binary mode
    topic.avatar = open('path/to/file.png', 'rb')
    topic.save()

Remove the avatar image for a topic::

    topic.avatar = ""
    topic.save()


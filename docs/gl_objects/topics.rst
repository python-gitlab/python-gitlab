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

* GitLab API: https://docs.gitlab.com/ce/api/topics.html

This endpoint requires admin access for creating, updating and deleting objects.

Examples
--------

List project topics on the GitLab instance::

    topics = gl.topics.list()

Get a specific topic by its ID::

    topic = gl.topics.get(topic_id)

Create a new topic::

    topic = gl.topics.create({"name": "my-topic"})

Update a topic::

    topic.description = "My new topic"
    topic.save()

    # or
    gl.topics.update(topic_id, {"description": "My new topic"})

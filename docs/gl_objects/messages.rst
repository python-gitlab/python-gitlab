##################
Broadcast messages
##################

You can use broadcast messages to display information on all pages of the
gitlab web UI. You must have administration permissions to manipulate broadcast
messages.

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.BroadcastMessage`
  + :class:`gitlab.v4.objects.BroadcastMessageManager`
  + :attr:`gitlab.Gitlab.broadcastmessages`

* GitLab API: https://docs.gitlab.com/ce/api/broadcast_messages.html

Examples
--------

List the messages::

    msgs = gl.broadcastmessages.list()

Get a single message::

    msg = gl.broadcastmessages.get(msg_id)

Create a message::

    msg = gl.broadcastmessages.create({'message': 'Important information'})

The date format for the ``starts_at`` and ``ends_at`` parameters is
``YYYY-MM-ddThh:mm:ssZ``.

Update a message::

    msg.font = '#444444'
    msg.color = '#999999'
    msg.save()

Delete a message::

    gl.broadcastmessages.delete(msg_id)
    # or
    msg.delete()

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

* v3 API:

  + :class:`gitlab.v3.objects.BroadcastMessage`
  + :class:`gitlab.v3.objects.BroadcastMessageManager`
  + :attr:`gitlab.Gitlab.broadcastmessages`

* GitLab API: https://docs.gitlab.com/ce/api/broadcast_messages.html

Examples
--------

List the messages:

.. literalinclude:: messages.py
   :start-after: # list
   :end-before: # end list

Get a single message:

.. literalinclude:: messages.py
   :start-after: # get
   :end-before: # end get

Create a message:

.. literalinclude:: messages.py
   :start-after: # create
   :end-before: # end create

The date format for ``starts_at`` and ``ends_at`` parameters is
``YYYY-MM-ddThh:mm:ssZ``.

Update a message:

.. literalinclude:: messages.py
   :start-after: # update
   :end-before: # end update

Delete a message:

.. literalinclude:: messages.py
   :start-after: # delete
   :end-before: # end delete

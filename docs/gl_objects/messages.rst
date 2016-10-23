##################
Broadcast messages
##################

You can use broadcast messages to display information on all pages of the
gitlab web UI. You must have administration permissions to manipulate broadcast
messages.

* Object class: :class:`gitlab.objects.BroadcastMessage`
* Manager object: :attr:`gitlab.Gitlab.broadcastmessages`

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

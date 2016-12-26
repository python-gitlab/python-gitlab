########
Snippets
########

You can store code snippets in Gitlab. Snippets can be attached to projects
(see :ref:`project_snippets`), but can also be detached.

* Object class: :class:`gitlab.objects.Namespace`
* Manager object: :attr:`gitlab.Gitlab.snippets`

Examples
========

List snippets woned by the current user:

.. literalinclude:: snippets.py
   :start-after: # list
   :end-before: # end list

List the public snippets:

.. literalinclude:: snippets.py
   :start-after: # public list
   :end-before: # end public list

Get a snippet:

.. literalinclude:: snippets.py
   :start-after: # get
   :end-before: # end get

.. warning::

   Blobs are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.


Create a snippet:

.. literalinclude:: snippets.py
   :start-after: # create
   :end-before: # end create

Update a snippet:

.. literalinclude:: snippets.py
   :start-after: # update
   :end-before: # end update

Delete a snippet:

.. literalinclude:: snippets.py
   :start-after: # delete
   :end-before: # end delete

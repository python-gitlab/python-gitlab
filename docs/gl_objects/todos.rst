#####
Todos
#####

Use :class:`~gitlab.objects.Todo` objects to manipulate todos. The
:attr:`gitlab.Gitlab.todos` manager object provides helper functions.

Examples
--------

List active todos:

.. literalinclude:: todos.py
   :start-after: # list
   :end-before: # end list

You can filter the list using the following parameters:

* ``action``: can be ``assigned``, ``mentioned``, ``build_failed``, ``marked``,
  or ``approval_required``
* ``author_id``
* ``project_id``
* ``state``: can be ``pending`` or ``done``
* ``type``: can be ``Issue`` or ``MergeRequest``

For example:

.. literalinclude:: todos.py
   :start-after: # filter
   :end-before: # end filter

Get a single todo:

.. literalinclude:: todos.py
   :start-after: # get
   :end-before: # end get

Mark a todo as done:

.. literalinclude:: todos.py
   :start-after: # delete
   :end-before: # end delete

Mark all the todos as done:

.. literalinclude:: todos.py
   :start-after: # all_delete
   :end-before: # end all_delete

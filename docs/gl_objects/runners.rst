#######
Runners
#######

Global runners
==============

Use :class:`~gitlab.objects.Runner` objects to manipulate runners. The
:attr:`gitlab.Gitlab.runners` manager object provides helper functions.

Examples
--------

Use the ``list()`` and ``all()`` methods to list runners.

The ``all()`` method accepts a ``scope`` parameter to filter the list. Allowed
values for this parameter are ``specific``, ``shared``, ``active``, ``paused``
and ``online``.

.. note::

   The returned objects hold minimal information about the runners. Use the
   ``get()`` method to retrieve detail about a runner.

.. literalinclude:: runners.py
   :start-after: # list
   :end-before: # end list

Get a runner's detail:

.. literalinclude:: runners.py
   :start-after: # get
   :end-before: # end get

Update a runner:

.. literalinclude:: runners.py
   :start-after: # update
   :end-before: # end update

Remove a runner:

.. literalinclude:: runners.py
   :start-after: # delete
   :end-before: # end delete

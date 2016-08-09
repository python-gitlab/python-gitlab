############
System hooks
############

Use :class:`~gitlab.objects.Hook` objects to manipulate system hooks. The
:attr:`gitlab.Gitlab.hooks` manager object provides helper functions.

Examples
--------

List the system hooks:

.. literalinclude:: system_hooks.py
   :start-after: # list
   :end-before: # end list

Create a system hook:

.. literalinclude:: system_hooks.py
   :start-after: # create
   :end-before: # end create

Test a system hook. The returned object is not usable (it misses the hook ID):

.. literalinclude:: system_hooks.py
   :start-after: # test
   :end-before: # end test

Delete a system hook:

.. literalinclude:: system_hooks.py
   :start-after: # delete
   :end-before: # end delete

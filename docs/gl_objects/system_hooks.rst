############
System hooks
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Hook`
  + :class:`gitlab.v4.objects.HookManager`
  + :attr:`gitlab.Gitlab.hooks`

* v3 API:

  + :class:`gitlab.v3.objects.Hook`
  + :class:`gitlab.v3.objects.HookManager`
  + :attr:`gitlab.Gitlab.hooks`

* GitLab API: https://docs.gitlab.com/ce/api/system_hooks.html

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

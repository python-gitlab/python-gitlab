###
FAQ
###

How can I close or reopen an issue?
===================================


Set the issue ``state_event`` attribute to ``close`` or ``reopen`` and save the object:

.. code-block:: python

   issue = my_project.issues.get(issue_id)
   issue.state_event = 'close'
   issue.save()

######
Issues
######

Reported issues
===============

Use :class:`~gitlab.objects.Issues` objects to manipulate issues the
authenticated user reported. The :attr:`gitlab.Gitlab.issues` manager object
provides helper functions.

Examples
--------

List the issues:

.. literalinclude:: issues.py
   :start-after: # list
   :end-before: # end list

Use the ``state`` and ``label`` parameters to filter the results. Use the
``order_by`` and ``sort`` attributes to sort the results:

.. literalinclude:: issues.py
   :start-after: # filtered list
   :end-before: # end filtered list

Group issues
============

Use :class:`~gitlab.objects.GroupIssue` objects to manipulate issues. The
:attr:`gitlab.Gitlab.project_issues` and :attr:`Group.issues
<gitlab.objects.Group.issues>` manager objects provide helper functions.

Examples
--------

List the group issues:

.. literalinclude:: issues.py
   :start-after: # group issues list
   :end-before: # end group issues list

Project issues
==============

Use :class:`~gitlab.objects.ProjectIssue` objects to manipulate issues. The
:attr:`gitlab.Gitlab.project_issues` and :attr:`Project.issues
<gitlab.objects.Project.issues>` manager objects provide helper functions.

Examples
--------

List the project issues:

.. literalinclude:: issues.py
   :start-after: # project issues list
   :end-before: # end project issues list

Get a project issue:

.. literalinclude:: issues.py
   :start-after: # project issues get
   :end-before: # end project issues get

Create a new issue:

.. literalinclude:: issues.py
   :start-after: # project issues create
   :end-before: # end project issues create

Update an issue:

.. literalinclude:: issues.py
   :start-after: # project issue update
   :end-before: # end project issue update

Close / reopen an issue:

.. literalinclude:: issues.py
   :start-after: # project issue open_close
   :end-before: # end project issue open_close

Delete an issue:

.. literalinclude:: issues.py
   :start-after: # project issue delete
   :end-before: # end project issue delete

Subscribe / unsubscribe from an issue:

.. literalinclude:: issues.py
   :start-after: # project issue subscribe
   :end-before: # end project issue subscribe

Move an issue to another project:

.. literalinclude:: issues.py
   :start-after: # project issue move
   :end-before: # end project issue move

Make an issue as todo:

.. literalinclude:: issues.py
   :start-after: # project issue todo
   :end-before: # end project issue todo

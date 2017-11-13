######
Issues
######

Reported issues
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Issue`
  + :class:`gitlab.v4.objects.IssueManager`
  + :attr:`gitlab.Gitlab.issues`

* v3 API:

  + :class:`gitlab.v3.objects.Issue`
  + :class:`gitlab.v3.objects.IssueManager`
  + :attr:`gitlab.Gitlab.issues`

* GitLab API: https://docs.gitlab.com/ce/api/issues.html

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

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupIssue`
  + :class:`gitlab.v4.objects.GroupIssueManager`
  + :attr:`gitlab.v4.objects.Group.issues`

* v3 API:

  + :class:`gitlab.v3.objects.GroupIssue`
  + :class:`gitlab.v3.objects.GroupIssueManager`
  + :attr:`gitlab.v3.objects.Group.issues`
  + :attr:`gitlab.Gitlab.group_issues`

* GitLab API: https://docs.gitlab.com/ce/api/issues.html

Examples
--------

List the group issues:

.. literalinclude:: issues.py
   :start-after: # group issues list
   :end-before: # end group issues list

Project issues
==============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssue`
  + :class:`gitlab.v4.objects.ProjectIssueManager`
  + :attr:`gitlab.v4.objects.Project.issues`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectIssue`
  + :class:`gitlab.v3.objects.ProjectIssueManager`
  + :attr:`gitlab.v3.objects.Project.issues`
  + :attr:`gitlab.Gitlab.project_issues`

* GitLab API: https://docs.gitlab.com/ce/api/issues.html

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

Get a project issue from its `iid` (v3 only. Issues are retrieved by iid in V4 by default):

.. literalinclude:: issues.py
   :start-after: # project issues get from iid
   :end-before: # end project issues get from iid

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

Get time tracking stats:

.. literalinclude:: issues.py
   :start-after: # project issue time tracking stats
   :end-before: # end project issue time tracking stats

Set a time estimate for an issue:

.. literalinclude:: issues.py
   :start-after: # project issue set time estimate
   :end-before: # end project issue set time estimate

Reset a time estimate for an issue:

.. literalinclude:: issues.py
   :start-after: # project issue reset time estimate
   :end-before: # end project issue reset time estimate

Add spent time for an issue:

.. literalinclude:: issues.py
   :start-after: # project issue set time spent
   :end-before: # end project issue set time spent

Reset spent time for an issue:

.. literalinclude:: issues.py
   :start-after: # project issue reset time spent
   :end-before: # end project issue reset time spent


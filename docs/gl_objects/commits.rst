#######
Commits
#######

Commits
=======

Use :class:`~gitlab.objects.ProjectCommit` objects to manipulate commits. The
:attr:`gitlab.Gitlab.project_commits` and
:attr:`gitlab.objects.Project.commits` manager objects provide helper
functions.

Examples
--------

List the commits for a project:

.. literalinclude:: commits.py
   :start-after: # list
   :end-before: # end list

You can use the ``ref_name``, ``since`` and ``until`` filters to limit the
results:

.. literalinclude:: commits.py
   :start-after: # filter list
   :end-before: # end filter list

Get a commit detail:

.. literalinclude:: commits.py
   :start-after: # get
   :end-before: # end get

Get the diff for a commit:

.. literalinclude:: commits.py
   :start-after: # diff
   :end-before: # end diff

Commit comments
===============

Use :class:`~gitlab.objects.ProjectCommitStatus` objects to manipulate commits. The
:attr:`gitlab.Gitlab.project_commit_comments` and
:attr:`gitlab.objects.Project.commit_comments` and
:attr:`gitlab.objects.ProjectCommit.comments` manager objects provide helper
functions.

Examples
--------

Get the comments for a commit:

.. literalinclude:: commits.py
   :start-after: # comments list
   :end-before: # end comments list

Add a comment on a commit:

.. literalinclude:: commits.py
   :start-after: # comments create
   :end-before: # end comments create

Commit status
=============

Use :class:`~gitlab.objects.ProjectCommitStatus` objects to manipulate commits.
The :attr:`gitlab.Gitlab.project_commit_statuses`,
:attr:`gitlab.objects.Project.commit_statuses` and
:attr:`gitlab.objects.ProjectCommit.statuses` manager objects provide helper
functions.

Examples
--------

Get the statuses for a commit:

.. literalinclude:: commits.py
   :start-after: # statuses list
   :end-before: # end statuses list

Change the status of a commit:

.. literalinclude:: commits.py
   :start-after: # statuses set
   :end-before: # end statuses set

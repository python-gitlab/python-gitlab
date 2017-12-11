#######
Commits
#######

Commits
=======

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCommit`
  + :class:`gitlab.v4.objects.ProjectCommitManager`
  + :attr:`gitlab.v4.objects.Project.commits`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectCommit`
  + :class:`gitlab.v3.objects.ProjectCommitManager`
  + :attr:`gitlab.v3.objects.Project.commits`
  + :attr:`gitlab.Gitlab.project_commits`

* GitLab API: https://docs.gitlab.com/ce/api/commits.html

.. warning::

   Pagination starts at page 0 in v3, but starts at page 1 in v4 (like all the
   v4 endpoints).


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

Create a commit:

.. literalinclude:: commits.py
   :start-after: # create
   :end-before: # end create

Get a commit detail:

.. literalinclude:: commits.py
   :start-after: # get
   :end-before: # end get

Get the diff for a commit:

.. literalinclude:: commits.py
   :start-after: # diff
   :end-before: # end diff

Cherry-pick a commit into another branch:

.. literalinclude:: commits.py
   :start-after: # cherry
   :end-before: # end cherry

Commit comments
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCommitComment`
  + :class:`gitlab.v4.objects.ProjectCommitCommentManager`
  + :attr:`gitlab.v4.objects.Commit.comments`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectCommit`
  + :class:`gitlab.v3.objects.ProjectCommitManager`
  + :attr:`gitlab.v3.objects.Commit.comments`
  + :attr:`gitlab.v3.objects.Project.commit_comments`
  + :attr:`gitlab.Gitlab.project_commit_comments`

* GitLab API: https://docs.gitlab.com/ce/api/commits.html

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

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCommitStatus`
  + :class:`gitlab.v4.objects.ProjectCommitStatusManager`
  + :attr:`gitlab.v4.objects.Commit.statuses`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectCommit`
  + :class:`gitlab.v3.objects.ProjectCommitManager`
  + :attr:`gitlab.v3.objects.Commit.statuses`
  + :attr:`gitlab.v3.objects.Project.commit_statuses`
  + :attr:`gitlab.Gitlab.project_commit_statuses`

* GitLab API: https://docs.gitlab.com/ce/api/commits.html

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

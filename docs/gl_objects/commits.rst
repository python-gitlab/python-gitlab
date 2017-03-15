#######
Commits
#######

Commits
=======

* Object class: :class:`~gitlab.objects.ProjectCommit`
* Manager objects: :attr:`gitlab.Gitlab.project_commits`,
  :attr:`gitlab.objects.Project.commits`

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

Cherry-pick a commit into another branch

.. literalinclude:: commits.py
   :start-after: # cherry
   :end-before: # end cherry

Commit comments
===============

* Object class: :class:`~gitlab.objects.ProjectCommiComment`
* Manager objects: :attr:`gitlab.Gitlab.project_commit_comments`,
  :attr:`gitlab.objects.Project.commit_comments`,
  :attr:`gitlab.objects.ProjectCommit.comments`

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

* Object class: :class:`~gitlab.objects.ProjectCommitStatus`
* Manager objects: :attr:`gitlab.Gitlab.project_commit_statuses`,
  :attr:`gitlab.objects.Project.commit_statuses`,
  :attr:`gitlab.objects.ProjectCommit.statuses`

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

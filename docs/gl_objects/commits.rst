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

Examples
--------

List the commits for a project::

    commits = project.commits.list()

You can use the ``ref_name``, ``since`` and ``until`` filters to limit the
results::

    commits = project.commits.list(ref_name='my_branch')
    commits = project.commits.list(since='2016-01-01T00:00:00Z')

List all commits for a project (see :ref:`pagination`) on all branches:

    commits = project.commits.list(get_all=True, all=True)

Create a commit::

    # See https://docs.gitlab.com/ce/api/commits.html#create-a-commit-with-multiple-files-and-actions
    # for actions detail
    data = {
        'branch': 'main',
        'commit_message': 'blah blah blah',
        'actions': [
            {
                'action': 'create',
                'file_path': 'README.rst',
                'content': open('path/to/file.rst').read(),
            },
            {
                # Binary files need to be base64 encoded
                'action': 'create',
                'file_path': 'logo.png',
                'content': base64.b64encode(open('logo.png', mode='r+b').read()).decode(),
                'encoding': 'base64',
            }
        ]
    }

    commit = project.commits.create(data)

Get a commit detail::

    commit = project.commits.get('e3d5a71b')

Get the diff for a commit::

    diff = commit.diff()

Cherry-pick a commit into another branch::

    commit.cherry_pick(branch='target_branch')

Revert a commit on a given branch::

    commit.revert(branch='target_branch')

Get the references the commit has been pushed to (branches and tags)::

    commit.refs()  # all references
    commit.refs('tag')  # only tags
    commit.refs('branch')  # only branches

Get the signature of the commit (if the commit was signed, e.g. with GPG or x509)::

    commit.signature()

List the merge requests related to a commit::

    commit.merge_requests()

Commit comments
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCommitComment`
  + :class:`gitlab.v4.objects.ProjectCommitCommentManager`
  + :attr:`gitlab.v4.objects.ProjectCommit.comments`

* GitLab API: https://docs.gitlab.com/ce/api/commits.html

Examples
--------

Get the comments for a commit::

    comments = commit.comments.list()

Add a comment on a commit::

    # Global comment
    commit = commit.comments.create({'note': 'This is a nice comment'})
    # Comment on a line in a file (on the new version of the file)
    commit = commit.comments.create({'note': 'This is another comment',
                                     'line': 12,
                                     'line_type': 'new',
                                     'path': 'README.rst'})

Commit status
=============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCommitStatus`
  + :class:`gitlab.v4.objects.ProjectCommitStatusManager`
  + :attr:`gitlab.v4.objects.ProjectCommit.statuses`

* GitLab API: https://docs.gitlab.com/ce/api/commits.html

Examples
--------

List the statuses for a commit::

    statuses = commit.statuses.list()

Change the status of a commit::

    commit.statuses.create({'state': 'success'})

###########
Discussions
###########

Discussions organize the notes in threads. See the :ref:`project-notes` chapter
for more information about notes.

Discussions are available for project issues, merge requests, snippets and
commits.

Reference
=========

* v4 API:

  Issues:

  + :class:`gitlab.v4.objects.ProjectIssueDiscussion`
  + :class:`gitlab.v4.objects.ProjectIssueDiscussionManager`
  + :class:`gitlab.v4.objects.ProjectIssueDiscussionNote`
  + :class:`gitlab.v4.objects.ProjectIssueDiscussionNoteManager`
  + :attr:`gitlab.v4.objects.ProjectIssue.notes`

  MergeRequests:

  + :class:`gitlab.v4.objects.ProjectMergeRequestDiscussion`
  + :class:`gitlab.v4.objects.ProjectMergeRequestDiscussionManager`
  + :class:`gitlab.v4.objects.ProjectMergeRequestDiscussionNote`
  + :class:`gitlab.v4.objects.ProjectMergeRequestDiscussionNoteManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.notes`

  Snippets:

  + :class:`gitlab.v4.objects.ProjectSnippetDiscussion`
  + :class:`gitlab.v4.objects.ProjectSnippetDiscussionManager`
  + :class:`gitlab.v4.objects.ProjectSnippetDiscussionNote`
  + :class:`gitlab.v4.objects.ProjectSnippetDiscussionNoteManager`
  + :attr:`gitlab.v4.objects.ProjectSnippet.notes`

* GitLab API: https://docs.gitlab.com/ce/api/discussions.html

Examples
========

List the discussions for a resource (issue, merge request, snippet or commit)::

    discussions = resource.discussions.list()

Get a single discussion::

    discussion = resource.discussions.get(discussion_id)

You can access the individual notes in the discussion through the ``notes``
attribute. It holds a list of notes in chronological order::

    # ``resource.notes`` is a DiscussionNoteManager, so we need to get the
    # object notes using ``attributes``
    for note in discussion.attributes['notes']:
        print(note['body'])

.. note::

   The notes are dicts, not objects.

You can add notes to existing discussions::

    new_note = discussion.notes.create({'body': 'Episode IV: A new note'})

You can get and update a single note using the ``*DiscussionNote`` resources::

    discussion = resource.discussions.get(discussion_id)
    # Get the latest note's id
    note_id = discussion.attributes['notes'][-1]['id']
    last_note = discussion.notes.get(note_id)
    last_note.body = 'Updated comment'
    last_note.save()

Create a new discussion::

    discussion = resource.discussions.create({'body': 'First comment of discussion'})

You can comment on merge requests and commit diffs. Provide the ``position``
dict to define where the comment should appear in the diff::

    mr_diff = mr.diffs.get(diff_id)
    mr.discussions.create({'body': 'Note content',
                           'position': {
                               'base_sha': mr_diff.base_commit_sha,
                               'start_sha': mr_diff.start_commit_sha,
                               'head_sha': mr_diff.head_commit_sha,
                               'position_type': 'text',
                               'new_line': 1,
                               'old_path': 'README.rst',
                               'new_path': 'README.rst'}
                           })

Resolve / unresolve a merge request discussion::

    mr_d = mr.discussions.get(d_id)
    mr_d.resolved = True  # True to resolve, False to unresolve
    mr_d.save()

Delete a comment::

    discussions.notes.delete(note_id)
    # or
    note.delete()

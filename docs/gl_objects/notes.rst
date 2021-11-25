.. _project-notes:

#####
Notes
#####

You can manipulate notes (comments) on group epics, project issues, merge requests and
snippets.

Reference
---------

* v4 API:

  Epics:

  * :class:`gitlab.v4.objects.GroupEpicNote`
  * :class:`gitlab.v4.objects.GroupEpicNoteManager`
  * :attr:`gitlab.v4.objects.GroupEpic.notes`

  Issues:

  + :class:`gitlab.v4.objects.ProjectIssueNote`
  + :class:`gitlab.v4.objects.ProjectIssueNoteManager`
  + :attr:`gitlab.v4.objects.ProjectIssue.notes`

  MergeRequests:

  + :class:`gitlab.v4.objects.ProjectMergeRequestNote`
  + :class:`gitlab.v4.objects.ProjectMergeRequestNoteManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.notes`

  Snippets:

  + :class:`gitlab.v4.objects.ProjectSnippetNote`
  + :class:`gitlab.v4.objects.ProjectSnippetNoteManager`
  + :attr:`gitlab.v4.objects.ProjectSnippet.notes`

* GitLab API: https://docs.gitlab.com/ce/api/notes.html

Examples
--------

List the notes for a resource::

    e_notes = epic.notes.list()
    i_notes = issue.notes.list()
    mr_notes = mr.notes.list()
    s_notes = snippet.notes.list()

Get a note for a resource::

    e_note = epic.notes.get(note_id)
    i_note = issue.notes.get(note_id)
    mr_note = mr.notes.get(note_id)
    s_note = snippet.notes.get(note_id)

Create a note for a resource::

    e_note = epic.notes.create({'body': 'note content'})
    i_note = issue.notes.create({'body': 'note content'})
    mr_note = mr.notes.create({'body': 'note content'})
    s_note = snippet.notes.create({'body': 'note content'})

Update a note for a resource::

    note.body = 'updated note content'
    note.save()

Delete a note for a resource::

    note.delete()

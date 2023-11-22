.. _draft-notes:

###########
Draft Notes
###########

Draft notes are pending, unpublished comments on merge requests.
They can be either start a discussion, or be associated with an existing discussion as a reply.
They are viewable only by the author until they are published. 

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeRequestDraftNote`
  + :class:`gitlab.v4.objects.ProjectMergeRequestDraftNoteManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.draft_notes`


* GitLab API: https://docs.gitlab.com/ee/api/draft_notes.html

Examples
--------

List all draft notes for a merge request::

    draft_notes = merge_request.draft_notes.list()

Get a draft note for a merge request by ID::

    draft_note = merge_request.draft_notes.get(note_id)

.. warning::

   When creating or updating draft notes, you can provide a complex nested ``position`` argument as a dictionary.
   Please consult the upstream API documentation linked above for the exact up-to-date attributes.

Create a draft note for a merge request::

    draft_note = merge_request.draft_notes.create({'note': 'note content'})

Update an existing draft note::

    draft_note.note = 'updated note content'
    draft_note.save()

Delete an existing draft note::

    draft_note.delete()

Publish an existing draft note::

    draft_note.publish()

Publish all existing draft notes for a merge request in bulk::

    merge_request.draft_notes.bulk_publish()

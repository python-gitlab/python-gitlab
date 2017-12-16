############
Award Emojis
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssueAwardEmoji`
  + :class:`gitlab.v4.objects.ProjectIssueNoteAwardEmoji`
  + :class:`gitlab.v4.objects.ProjectMergeRequestAwardEmoji`
  + :class:`gitlab.v4.objects.ProjectMergeRequestNoteAwardEmoji`
  + :class:`gitlab.v4.objects.ProjectSnippetAwardEmoji`
  + :class:`gitlab.v4.objects.ProjectSnippetNoteAwardEmoji`
  + :class:`gitlab.v4.objects.ProjectIssueAwardEmojiManager`
  + :class:`gitlab.v4.objects.ProjectIssueNoteAwardEmojiManager`
  + :class:`gitlab.v4.objects.ProjectMergeRequestAwardEmojiManager`
  + :class:`gitlab.v4.objects.ProjectMergeRequestNoteAwardEmojiManager`
  + :class:`gitlab.v4.objects.ProjectSnippetAwardEmojiManager`
  + :class:`gitlab.v4.objects.ProjectSnippetNoteAwardEmojiManager`


* GitLab API: https://docs.gitlab.com/ce/api/award_emoji.html

Examples
--------

List emojis for a resource::

   emojis = obj.awardemojis.list()

Get a single emoji::

   emoji = obj.awardemojis.get(emoji_id)

Add (create) an emoji::

   emoji = obj.awardemojis.create({'name': 'tractor'})

Delete an emoji::

   emoji.delete
   # or
   obj.awardemojis.delete(emoji_id)

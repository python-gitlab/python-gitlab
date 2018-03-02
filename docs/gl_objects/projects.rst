########
Projects
########

Projects
========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Project`
  + :class:`gitlab.v4.objects.ProjectManager`
  + :attr:`gitlab.Gitlab.projects`

* v3 API:

  + :class:`gitlab.v3.objects.Project`
  + :class:`gitlab.v3.objects.ProjectManager`
  + :attr:`gitlab.Gitlab.projects`

* GitLab API: https://docs.gitlab.com/ce/api/projects.html

Examples
--------

List projects:

The API provides several filtering parameters for the listing methods:

* ``archived``: if ``True`` only archived projects will be returned
* ``visibility``: returns only projects with the specified visibility (can be
  ``public``, ``internal`` or ``private``)
* ``search``: returns project matching the given pattern

Results can also be sorted using the following parameters:

* ``order_by``: sort using the given argument. Valid values are ``id``,
  ``name``, ``path``, ``created_at``, ``updated_at`` and ``last_activity_at``.
  The default is to sort by ``created_at``
* ``sort``: sort order (``asc`` or ``desc``)

.. literalinclude:: projects.py
   :start-after: # list
   :end-before: # end list

Get a single project:

.. literalinclude:: projects.py
   :start-after: # get
   :end-before: # end get

Create a project:

.. literalinclude:: projects.py
   :start-after: # create
   :end-before: # end create

Create a project for a user (admin only):

.. literalinclude:: projects.py
   :start-after: # user create
   :end-before: # end user create

Create a project in a group:

You need to get the id of the group, then use the namespace_id attribute to create the group:

.. code:: python

  group_id = gl.groups.search('my-group')[0].id
  project = gl.projects.create({'name': 'myrepo', 'namespace_id': group_id})


Update a project:

.. literalinclude:: projects.py
   :start-after: # update
   :end-before: # end update

Delete a project:

.. literalinclude:: projects.py
   :start-after: # delete
   :end-before: # end delete

Fork a project:

.. literalinclude:: projects.py
   :start-after: # fork
   :end-before: # end fork

Create/delete a fork relation between projects (requires admin permissions):

.. literalinclude:: projects.py
   :start-after: # forkrelation
   :end-before: # end forkrelation

Star/unstar a project:

.. literalinclude:: projects.py
   :start-after: # star
   :end-before: # end star

Archive/unarchive a project:

.. literalinclude:: projects.py
   :start-after: # archive
   :end-before: # end archive

.. note::

   Previous versions used ``archive_`` and ``unarchive_`` due to a naming issue,
   they have been deprecated but not yet removed.

Start the housekeeping job:

.. literalinclude:: projects.py
   :start-after: # housekeeping
   :end-before: # end housekeeping

List the repository tree:

.. literalinclude:: projects.py
   :start-after: # repository tree
   :end-before: # end repository tree

Get the content and metadata of a file for a commit, using a blob sha:

.. literalinclude:: projects.py
   :start-after: # repository blob
   :end-before: # end repository blob

Get the repository archive:

.. literalinclude:: projects.py
   :start-after: # repository archive
   :end-before: # end repository archive

.. warning::

   Archives are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Get the content of a file using the blob id:

.. literalinclude:: projects.py
   :start-after: # repository raw_blob
   :end-before: # end repository raw_blob

.. warning::

   Blobs are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Compare two branches, tags or commits:

.. literalinclude:: projects.py
   :start-after: # repository compare
   :end-before: # end repository compare

Get a list of contributors for the repository:

.. literalinclude:: projects.py
   :start-after: # repository contributors
   :end-before: # end repository contributors

Get a list of users for the repository:

.. literalinclude:: projects.py
   :start-after: # users list
   :end-before: # end users list

Project custom attributes
=========================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCustomAttribute`
  + :class:`gitlab.v4.objects.ProjectCustomAttributeManager`
  + :attr:`gitlab.v4.objects.Project.customattributes`

* GitLab API: https://docs.gitlab.com/ce/api/custom_attributes.html

Examples
--------

List custom attributes for a project::

    attrs = project.customattributes.list()

Get a custom attribute for a project::

    attr = project.customattributes.get(attr_key)

Set (create or update) a custom attribute for a project::

    attr = project.customattributes.set(attr_key, attr_value)

Delete a custom attribute for a project::

    attr.delete()
    # or
    project.customattributes.delete(attr_key)

Search projects by custom attribute::

    project.customattributes.set('type': 'internal')
    gl.projects.list(custom_attributes={'type': 'internal'})

Project files
=============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectFile`
  + :class:`gitlab.v4.objects.ProjectFileManager`
  + :attr:`gitlab.v4.objects.Project.files`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectFile`
  + :class:`gitlab.v3.objects.ProjectFileManager`
  + :attr:`gitlab.v3.objects.Project.files`
  + :attr:`gitlab.Gitlab.project_files`

* GitLab API: https://docs.gitlab.com/ce/api/repository_files.html

Examples
--------

Get a file:

.. literalinclude:: projects.py
   :start-after: # files get
   :end-before: # end files get

Create a new file:

.. literalinclude:: projects.py
   :start-after: # files create
   :end-before: # end files create

Update a file. The entire content must be uploaded, as plain text or as base64
encoded text:

.. literalinclude:: projects.py
   :start-after: # files update
   :end-before: # end files update

Delete a file:

.. literalinclude:: projects.py
   :start-after: # files delete
   :end-before: # end files delete

Project tags
============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectTag`
  + :class:`gitlab.v4.objects.ProjectTagManager`
  + :attr:`gitlab.v4.objects.Project.tags`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectTag`
  + :class:`gitlab.v3.objects.ProjectTagManager`
  + :attr:`gitlab.v3.objects.Project.tags`
  + :attr:`gitlab.Gitlab.project_tags`

* GitLab API: https://docs.gitlab.com/ce/api/tags.html

Examples
--------

List the project tags:

.. literalinclude:: projects.py
   :start-after: # tags list
   :end-before: # end tags list

Get a tag:

.. literalinclude:: projects.py
   :start-after: # tags get
   :end-before: # end tags get

Create a tag:

.. literalinclude:: projects.py
   :start-after: # tags create
   :end-before: # end tags create

Set or update the release note for a tag:

.. literalinclude:: projects.py
   :start-after: # tags release
   :end-before: # end tags release

Delete a tag:

.. literalinclude:: projects.py
   :start-after: # tags delete
   :end-before: # end tags delete

.. _project_snippets:

Project snippets
================

The snippet visibility can be defined using the following constants:

* ``gitlab.VISIBILITY_PRIVATE``
* ``gitlab.VISIBILITY_INTERNAL``
* ``gitlab.VISIBILITY_PUBLIC``

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectSnippet`
  + :class:`gitlab.v4.objects.ProjectSnippetManager`
  + :attr:`gitlab.v4.objects.Project.files`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectSnippet`
  + :class:`gitlab.v3.objects.ProjectSnippetManager`
  + :attr:`gitlab.v3.objects.Project.files`
  + :attr:`gitlab.Gitlab.project_files`

* GitLab API: https://docs.gitlab.com/ce/api/project_snippets.html

Examples
--------

List the project snippets:

.. literalinclude:: projects.py
   :start-after: # snippets list
   :end-before: # end snippets list

Get a snippet:

.. literalinclude:: projects.py
   :start-after: # snippets get
   :end-before: # end snippets get

Get the content of a snippet:

.. literalinclude:: projects.py
   :start-after: # snippets content
   :end-before: # end snippets content

.. warning::

   The snippet content is entirely stored in memory unless you use the
   streaming feature. See :ref:`the artifacts example <streaming_example>`.

Create a snippet:

.. literalinclude:: projects.py
   :start-after: # snippets create
   :end-before: # end snippets create

Update a snippet:

.. literalinclude:: projects.py
   :start-after: # snippets update
   :end-before: # end snippets update

Delete a snippet:

.. literalinclude:: projects.py
   :start-after: # snippets delete
   :end-before: # end snippets delete

Notes
=====

You can manipulate notes (comments) on the issues, merge requests and snippets.

* :class:`~gitlab.objects.ProjectIssue` with
  :class:`~gitlab.objects.ProjectIssueNote`
* :class:`~gitlab.objects.ProjectMergeRequest` with
  :class:`~gitlab.objects.ProjectMergeRequestNote`
* :class:`~gitlab.objects.ProjectSnippet` with
  :class:`~gitlab.objects.ProjectSnippetNote`

Reference
---------

* v4 API:

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

* v3 API:

  Issues:

  + :class:`gitlab.v3.objects.ProjectIssueNote`
  + :class:`gitlab.v3.objects.ProjectIssueNoteManager`
  + :attr:`gitlab.v3.objects.ProjectIssue.notes`
  + :attr:`gitlab.v3.objects.Project.issue_notes`
  + :attr:`gitlab.Gitlab.project_issue_notes`

  MergeRequests:

  + :class:`gitlab.v3.objects.ProjectMergeRequestNote`
  + :class:`gitlab.v3.objects.ProjectMergeRequestNoteManager`
  + :attr:`gitlab.v3.objects.ProjectMergeRequest.notes`
  + :attr:`gitlab.v3.objects.Project.mergerequest_notes`
  + :attr:`gitlab.Gitlab.project_mergerequest_notes`

  Snippets:

  + :class:`gitlab.v3.objects.ProjectSnippetNote`
  + :class:`gitlab.v3.objects.ProjectSnippetNoteManager`
  + :attr:`gitlab.v3.objects.ProjectSnippet.notes`
  + :attr:`gitlab.v3.objects.Project.snippet_notes`
  + :attr:`gitlab.Gitlab.project_snippet_notes`

* GitLab API: https://docs.gitlab.com/ce/api/repository_files.html

Examples
--------

List the notes for a resource:

.. literalinclude:: projects.py
   :start-after: # notes list
   :end-before: # end notes list

Get a note for a resource:

.. literalinclude:: projects.py
   :start-after: # notes get
   :end-before: # end notes get

Create a note for a resource:

.. literalinclude:: projects.py
   :start-after: # notes create
   :end-before: # end notes create

Update a note for a resource:

.. literalinclude:: projects.py
   :start-after: # notes update
   :end-before: # end notes update

Delete a note for a resource:

.. literalinclude:: projects.py
   :start-after: # notes delete
   :end-before: # end notes delete

Project members
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMember`
  + :class:`gitlab.v4.objects.ProjectMemberManager`
  + :attr:`gitlab.v4.objects.Project.members`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectMember`
  + :class:`gitlab.v3.objects.ProjectMemberManager`
  + :attr:`gitlab.v3.objects.Project.members`
  + :attr:`gitlab.Gitlab.project_members`

* GitLab API: https://docs.gitlab.com/ce/api/members.html

Examples
--------

List the project members:

.. literalinclude:: projects.py
   :start-after: # members list
   :end-before: # end members list

Search project members matching a query string:

.. literalinclude:: projects.py
   :start-after: # members search
   :end-before: # end members search

Get a single project member:

.. literalinclude:: projects.py
   :start-after: # members get
   :end-before: # end members get

Add a project member:

.. literalinclude:: projects.py
   :start-after: # members add
   :end-before: # end members add

Modify a project member (change the access level):

.. literalinclude:: projects.py
   :start-after: # members update
   :end-before: # end members update

Remove a member from the project team:

.. literalinclude:: projects.py
   :start-after: # members delete
   :end-before: # end members delete

Share the project with a group:

.. literalinclude:: projects.py
   :start-after: # share
   :end-before: # end share

Project hooks
=============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectHook`
  + :class:`gitlab.v4.objects.ProjectHookManager`
  + :attr:`gitlab.v4.objects.Project.hooks`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectHook`
  + :class:`gitlab.v3.objects.ProjectHookManager`
  + :attr:`gitlab.v3.objects.Project.hooks`
  + :attr:`gitlab.Gitlab.project_hooks`

* GitLab API: https://docs.gitlab.com/ce/api/projects.html#hooks

Examples
--------

List the project hooks:

.. literalinclude:: projects.py
   :start-after: # hook list
   :end-before: # end hook list

Get a project hook:

.. literalinclude:: projects.py
   :start-after: # hook get
   :end-before: # end hook get

Create a project hook:

.. literalinclude:: projects.py
   :start-after: # hook create
   :end-before: # end hook create

Update a project hook:

.. literalinclude:: projects.py
   :start-after: # hook update
   :end-before: # end hook update

Delete a project hook:

.. literalinclude:: projects.py
   :start-after: # hook delete
   :end-before: # end hook delete

Project Services
================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectService`
  + :class:`gitlab.v4.objects.ProjectServiceManager`
  + :attr:`gitlab.v4.objects.Project.services`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectService`
  + :class:`gitlab.v3.objects.ProjectServiceManager`
  + :attr:`gitlab.v3.objects.Project.services`
  + :attr:`gitlab.Gitlab.project_services`

* GitLab API: https://docs.gitlab.com/ce/api/services.html

Exammples
---------

Get a service:

.. literalinclude:: projects.py
   :start-after: # service get
   :end-before: # end service get

List the code names of available services (doesn't return objects):

.. literalinclude:: projects.py
   :start-after: # service list
   :end-before: # end service list

Configure and enable a service:

.. literalinclude:: projects.py
   :start-after: # service update
   :end-before: # end service update

Disable a service:

.. literalinclude:: projects.py
   :start-after: # service delete
   :end-before: # end service delete

Issue boards
============

Boards are a visual representation of existing issues for a project. Issues can
be moved from one list to the other to track progress and help with
priorities.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectBoard`
  + :class:`gitlab.v4.objects.ProjectBoardManager`
  + :attr:`gitlab.v4.objects.Project.boards`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectBoard`
  + :class:`gitlab.v3.objects.ProjectBoardManager`
  + :attr:`gitlab.v3.objects.Project.boards`
  + :attr:`gitlab.Gitlab.project_boards`

* GitLab API: https://docs.gitlab.com/ce/api/boards.html

Examples
--------

Get the list of existing boards for a project:

.. literalinclude:: projects.py
   :start-after: # boards list
   :end-before: # end boards list

Get a single board for a project:

.. literalinclude:: projects.py
   :start-after: # boards get
   :end-before: # end boards get

Board lists
===========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectBoardList`
  + :class:`gitlab.v4.objects.ProjectBoardListManager`
  + :attr:`gitlab.v4.objects.Project.board_lists`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectBoardList`
  + :class:`gitlab.v3.objects.ProjectBoardListManager`
  + :attr:`gitlab.v3.objects.ProjectBoard.lists`
  + :attr:`gitlab.v3.objects.Project.board_lists`
  + :attr:`gitlab.Gitlab.project_board_lists`

* GitLab API: https://docs.gitlab.com/ce/api/boards.html

Examples
--------

List the issue lists for a board:

.. literalinclude:: projects.py
   :start-after: # board lists list
   :end-before: # end board lists list

Get a single list:

.. literalinclude:: projects.py
   :start-after: # board lists get
   :end-before: # end board lists get

Create a new list:

.. literalinclude:: projects.py
   :start-after: # board lists create
   :end-before: # end board lists create

Change a list position. The first list is at position 0. Moving a list will
set it at the given position and move the following lists up a position:

.. literalinclude:: projects.py
   :start-after: # board lists update
   :end-before: # end board lists update

Delete a list:

.. literalinclude:: projects.py
   :start-after: # board lists delete
   :end-before: # end board lists delete


File uploads
============

Reference
---------

* v4 API:

  + :attr:`gitlab.v4.objects.Project.upload`

* v3 API:

  + :attr:`gitlab.v3.objects.Project.upload`

* Gitlab API: https://docs.gitlab.com/ce/api/projects.html#upload-a-file

Examples
--------

Upload a file into a project using a filesystem path:

.. literalinclude:: projects.py
   :start-after: # project file upload by path
   :end-before: # end project file upload by path

Upload a file into a project without a filesystem path:

.. literalinclude:: projects.py
   :start-after: # project file upload with data
   :end-before: # end project file upload with data

Upload a file and comment on an issue using the uploaded file's
markdown:

.. literalinclude:: projects.py
   :start-after: # project file upload markdown
   :end-before: # end project file upload markdown

Upload a file and comment on an issue while using custom
markdown to reference the uploaded file:

.. literalinclude:: projects.py
   :start-after: # project file upload markdown custom
   :end-before: # end project file upload markdown custom

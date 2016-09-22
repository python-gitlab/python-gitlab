########
Projects
########

Use :class:`~gitlab.objects.Project` objects to manipulate projects. The
:attr:`gitlab.Gitlab.projects` manager objects provides helper functions.

Examples
========

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

   The underscore character at the end of the methods is used to workaround a
   conflict with a previous misuse of the ``archive`` method (deprecated but
   not yet removed).

Repository
----------

The following examples show how you can manipulate the project code repository.

List the repository tree:

.. literalinclude:: projects.py
   :start-after: # repository tree
   :end-before: # end repository tree

Get the content of a file for a commit:

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

Files
-----

The following examples show how you can manipulate the project files.

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

Tags
----

Use :class:`~gitlab.objects.ProjectTag` objects to manipulate tags. The
:attr:`gitlab.Gitlab.project_tags` and :attr:`Project.tags
<gitlab.objects.Project.tags>` manager objects provide helper functions.

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

Snippets
--------

Use :class:`~gitlab.objects.ProjectSnippet` objects to manipulate snippets. The
:attr:`gitlab.Gitlab.project_snippets` and :attr:`Project.snippets
<gitlab.objects.Project.snippets>` manager objects provide helper functions.

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
-----

You can manipulate notes (comments) on the following resources:

* :class:`~gitlab.objects.ProjectIssue` with
  :class:`~gitlab.objects.ProjectIssueNote`
* :class:`~gitlab.objects.ProjectMergeRequest` with
  :class:`~gitlab.objects.ProjectMergeRequestNote`
* :class:`~gitlab.objects.ProjectSnippet` with
  :class:`~gitlab.objects.ProjectSnippetNote`

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

Events
------

Use :class:`~gitlab.objects.ProjectEvent` objects to manipulate events. The
:attr:`gitlab.Gitlab.project_events` and :attr:`Project.events
<gitlab.objects.Project.events>` manager objects provide helper functions.

List the project events:

.. literalinclude:: projects.py
   :start-after: # events list
   :end-before: # end events list

Team members
------------

Use :class:`~gitlab.objects.ProjectMember` objects to manipulate projects
members. The :attr:`gitlab.Gitlab.project_members` and :attr:`Project.members
<gitlab.objects.Projects.members>` manager objects provide helper functions.

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

Hooks
-----

Use :class:`~gitlab.objects.ProjectHook` objects to manipulate projects
hooks. The :attr:`gitlab.Gitlab.project_hooks` and :attr:`Project.hooks
<gitlab.objects.Projects.hooks>` manager objects provide helper functions.

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

Pipelines
---------

Use :class:`~gitlab.objects.ProjectPipeline` objects to manipulate projects
pipelines. The :attr:`gitlab.Gitlab.project_pipelines` and
:attr:`Project.services <gitlab.objects.Projects.pipelines>` manager objects
provide helper functions.

List pipelines for a project:

.. literalinclude:: projects.py
   :start-after: # pipeline list
   :end-before: # end pipeline list

Get a pipeline for a project:

.. literalinclude:: projects.py
   :start-after: # pipeline get
   :end-before: # end pipeline get

Retry the failed builds for a pipeline:

.. literalinclude:: projects.py
   :start-after: # pipeline retry
   :end-before: # end pipeline retry

Cancel builds in a pipeline:

.. literalinclude:: projects.py
   :start-after: # pipeline cancel
   :end-before: # end pipeline cancel

Services
--------

Use :class:`~gitlab.objects.ProjectService` objects to manipulate projects
services. The :attr:`gitlab.Gitlab.project_services` and
:attr:`Project.services <gitlab.objects.Projects.services>` manager objects
provide helper functions.

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

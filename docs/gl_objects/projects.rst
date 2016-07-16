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

Update a project:

.. literalinclude:: projects.py
   :start-after: # update
   :end-before: # end update

Delete a project:

.. literalinclude:: projects.py
   :start-after: # delete
   :end-before: # end delete

Fork a project :

.. literalinclude:: projects.py
   :start-after: # fork
   :end-before: # end fork

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

Events
------

Use :class:`~gitlab.objects.ProjectEvent` objects to manipulate projects. The
:attr:`gitlab.Gitlab.project_events` and :attr:`Project.events
<gitlab.objects.Project.events>` manager objects provide helper functions.

List the project events:

.. literalinclude:: projects.py
   :start-after: # events list
   :end-before: # end events list

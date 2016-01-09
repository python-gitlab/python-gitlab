#############################################
Upgrading from python-gitlab 0.10 and earlier
#############################################

``python-gitlab`` 0.11 introduces new objects which make the API cleaner and
easier to use. The feature set is unchanged but some methods have been
deprecated in favor of the new manager objects.

Deprecated methods will be remove in a future release.

Gitlab object migration
=======================

The objects constructor methods are deprecated:

* ``Hook()``
* ``Project()``
* ``UserProject()``
* ``Group()``
* ``Issue()``
* ``User()``
* ``Team()``

Use the new managers objects instead. For example:

.. code-block:: python

   # Deprecated syntax
   p1 = gl.Project({'name': 'myCoolProject'})
   p1.save()
   p2 = gl.Project(id=1)
   p_list = gl.Project()

   # New syntax
   p1 = gl.projects.create({'name': 'myCoolProject'})
   p2 = gl.projects.get(1)
   p_list = gl.projects.list()

The following methods are also deprecated:

* ``search_projects()``
* ``owned_projects()``
* ``all_projects()``

Use the ``projects`` manager instead:

.. code-block:: python

   # Deprecated syntax
   l1 = gl.search_projects('whatever')
   l2 = gl.owned_projects()
   l3 = gl.all_projects()

   # New syntax
   l1 = gl.projects.search('whatever')
   l2 = gl.projects.owned()
   l3 = gl.projects.all()

GitlabObject objects migration
==============================

The following constructor methods are deprecated in favor of the matching
managers:

.. list-table::
   :header-rows: 1

   * - Deprecated method
     - Matching manager
   * - ``User.Key()``
     - ``User.keys``
   * - ``CurrentUser.Key()``
     - ``CurrentUser.keys``
   * - ``Group.Member()``
     - ``Group.members``
   * - ``ProjectIssue.Note()``
     - ``ProjectIssue.notes``
   * - ``ProjectMergeRequest.Note()``
     - ``ProjectMergeRequest.notes``
   * - ``ProjectSnippet.Note()``
     - ``ProjectSnippet.notes``
   * - ``Project.Branch()``
     - ``Project.branches``
   * - ``Project.Commit()``
     - ``Project.commits``
   * - ``Project.Event()``
     - ``Project.events``
   * - ``Project.File()``
     - ``Project.files``
   * - ``Project.Hook()``
     - ``Project.hooks``
   * - ``Project.Key()``
     - ``Project.keys``
   * - ``Project.Issue()``
     - ``Project.issues``
   * - ``Project.Label()``
     - ``Project.labels``
   * - ``Project.Member()``
     - ``Project.members``
   * - ``Project.MergeRequest()``
     - ``Project.mergerequests``
   * - ``Project.Milestone()``
     - ``Project.milestones``
   * - ``Project.Note()``
     - ``Project.notes``
   * - ``Project.Snippet()``
     - ``Project.snippets``
   * - ``Project.Tag()``
     - ``Project.tags``
   * - ``Team.Member()``
     - ``Team.members``
   * - ``Team.Project()``
     - ``Team.projects``

For example:

.. code-block:: python

   # Deprecated syntax
   p = gl.Project(id=2)
   issues = p.Issue()

   # New syntax
   p = gl.projects.get(2)
   issues = p.issues.list()

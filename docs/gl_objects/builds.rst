######
Builds
######

Build triggers
==============

Use :class:`~gitlab.objects.ProjectTrigger` objects to manipulate build
triggers. The :attr:`gitlab.Gitlab.project_triggers` and
:attr:`gitlab.objects.Projeect.triggers` manager objects provide helper
functions.

Examples
--------

List triggers:

.. literalinclude:: builds.py
   :start-after: # trigger list
   :end-before: # end trigger list

Get a trigger:

.. literalinclude:: builds.py
   :start-after: # trigger get
   :end-before: # end trigger get

Create a trigger:

.. literalinclude:: builds.py
   :start-after: # trigger create
   :end-before: # end trigger create

Remove a trigger:

.. literalinclude:: builds.py
   :start-after: # trigger delete
   :end-before: # end trigger delete

Build variables
===============

Use :class:`~gitlab.objects.ProjectVariable` objects to manipulate build
variables. The :attr:`gitlab.Gitlab.project_variables` and
:attr:`gitlab.objects.Projeect.variables` manager objects provide helper
functions.

Examples
--------

List variables:

.. literalinclude:: builds.py
   :start-after: # var list
   :end-before: # end var list

Get a variable:

.. literalinclude:: builds.py
   :start-after: # var get
   :end-before: # end var get

Create a variable:

.. literalinclude:: builds.py
   :start-after: # var create
   :end-before: # end var create

Update a variable value:

.. literalinclude:: builds.py
   :start-after: # var update
   :end-before: # end var update

Remove a variable:

.. literalinclude:: builds.py
   :start-after: # var delete
   :end-before: # end var delete

Builds
======

Use :class:`~gitlab.objects.ProjectBuild` objects to manipulate builds. The
:attr:`gitlab.Gitlab.project_builds` and :attr:`gitlab.objects.Projeect.builds`
manager objects provide helper functions.

Examples
--------

List builds for the project:

.. literalinclude:: builds.py
   :start-after: # list
   :end-before: # end list

To list builds for a specific commit, create a
:class:`~gitlab.objects.ProjectCommit` object and use its
:attr:`~gitlab.objects.ProjectCommit.builds` method:

.. literalinclude:: builds.py
   :start-after: # commit list
   :end-before: # end commit list

Get a build:

.. literalinclude:: builds.py
   :start-after: # get
   :end-before: # end get

Get a build artifacts:

.. literalinclude:: builds.py
   :start-after: # artifacts
   :end-before: # end artifacts

.. warning::

   Artifacts are entirely stored in memory.

Mark a build artifact as kept when expiration is set:

.. literalinclude:: builds.py
   :start-after: # keep artifacts
   :end-before: # end keep artifacts

Get a build trace:

.. literalinclude:: builds.py
   :start-after: # trace
   :end-before: # end trace

.. warning::

   Traces are entirely stored in memory.

Cancel/retry a build:

.. literalinclude:: builds.py
   :start-after: # retry
   :end-before: # end retry

Erase a build:

.. literalinclude:: builds.py
   :start-after: # delete
   :end-before: # end delete

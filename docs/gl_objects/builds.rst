######
Builds
######

Build triggers
==============

Use :class:`~gitlab.objects.ProjectTrigger` objects to manipulate build
triggers. The :attr:`gitlab.Gitlab.project_triggers` and
:attr:`gitlab.objects.Project.triggers` manager objects provide helper
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
:attr:`gitlab.objects.Project.variables` manager objects provide helper
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
:attr:`gitlab.Gitlab.project_builds` and :attr:`gitlab.objects.Project.builds`
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

   Artifacts are entirely stored in memory in this example.

.. _streaming_example:

You can download artifacts as a stream. Provide a callable to handle the
stream:

.. literalinclude:: builds.py
   :start-after: # stream artifacts
   :end-before: # end stream artifacts

Mark a build artifact as kept when expiration is set:

.. literalinclude:: builds.py
   :start-after: # keep artifacts
   :end-before: # end keep artifacts

Get a build trace:

.. literalinclude:: builds.py
   :start-after: # trace
   :end-before: # end trace

.. warning::

   Traces are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Cancel/retry a build:

.. literalinclude:: builds.py
   :start-after: # retry
   :end-before: # end retry

Play (trigger) a build:

.. literalinclude:: builds.py
   :start-after: # play
   :end-before: # end play

Erase a build (artifacts and trace):

.. literalinclude:: builds.py
   :start-after: # erase
   :end-before: # end erase

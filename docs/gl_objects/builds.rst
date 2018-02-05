##########################
Pipelines, Builds and Jobs
##########################

Build and job are two classes representing the same object. Builds are used in
v3 API, jobs in v4 API.

Project pipelines
=================

A pipeline is a group of jobs executed by GitLab CI.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPipeline`
  + :class:`gitlab.v4.objects.ProjectPipelineManager`
  + :attr:`gitlab.v4.objects.Project.pipelines`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectPipeline`
  + :class:`gitlab.v3.objects.ProjectPipelineManager`
  + :attr:`gitlab.v3.objects.Project.pipelines`
  + :attr:`gitlab.Gitlab.project_pipelines`

* GitLab API: https://docs.gitlab.com/ce/api/pipelines.html

Examples
--------

List pipelines for a project::

    pipelines = project.pipelines.list()

Get a pipeline for a project::

    pipeline = project.pipelines.get(pipeline_id)

Create a pipeline for a particular reference::

    pipeline = project.pipelines.create({'ref': 'master'})

Retry the failed builds for a pipeline::

    pipeline.retry()

Cancel builds in a pipeline::

    pipeline.cancel()

Triggers
========

Triggers provide a way to interact with the GitLab CI. Using a trigger a user
or an application can run a new build/job for a specific commit.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectTrigger`
  + :class:`gitlab.v4.objects.ProjectTriggerManager`
  + :attr:`gitlab.v4.objects.Project.triggers`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectTrigger`
  + :class:`gitlab.v3.objects.ProjectTriggerManager`
  + :attr:`gitlab.v3.objects.Project.triggers`
  + :attr:`gitlab.Gitlab.project_triggers`

* GitLab API: https://docs.gitlab.com/ce/api/pipeline_triggers.html

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

Full example with wait for finish:

.. literalinclude:: builds.py
   :start-after: # pipeline trigger
   :end-before: # end pipeline trigger

Pipeline schedule
=================

You can schedule pipeline runs using a cron-like syntax. Variables can be
associated with the scheduled pipelines.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectPipelineSchedule`
  + :class:`gitlab.v4.objects.ProjectPipelineScheduleManager`
  + :attr:`gitlab.v4.objects.Project.pipelineschedules`
  + :class:`gitlab.v4.objects.ProjectPipelineScheduleVariable`
  + :class:`gitlab.v4.objects.ProjectPipelineScheduleVariableManager`
  + :attr:`gitlab.v4.objects.Project.pipelineschedules`

* GitLab API: https://docs.gitlab.com/ce/api/pipeline_schedules.html

Examples
--------

List pipeline schedules::

    scheds = project.pipelineschedules.list()

Get a single schedule::

    sched = projects.pipelineschedules.get(schedule_id)

Create a new schedule::

    sched = project.pipelineschedules.create({
        'ref': 'master',
        'description': 'Daily test',
        'cron': '0 1 * * *'})

Update a schedule::

    sched.cron = '1 2 * * *'
    sched.save()

Delete a schedule::

    sched.delete()

Create a schedule variable::

    var = sched.variables.create({'key': 'foo', 'value': 'bar'})

Edit a schedule variable::

    var.value = 'new_value'
    var.save()

Delete a schedule variable::

    var.delete()

Projects and groups variables
=============================

You can associate variables to projects and groups to modify the build/job
scripts behavior.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectVariable`
  + :class:`gitlab.v4.objects.ProjectVariableManager`
  + :attr:`gitlab.v4.objects.Project.variables`
  + :class:`gitlab.v4.objects.GroupVariable`
  + :class:`gitlab.v4.objects.GroupVariableManager`
  + :attr:`gitlab.v4.objects.Group.variables`

* v3 API

  + :class:`gitlab.v3.objects.ProjectVariable`
  + :class:`gitlab.v3.objects.ProjectVariableManager`
  + :attr:`gitlab.v3.objects.Project.variables`
  + :attr:`gitlab.Gitlab.project_variables`

* GitLab API

  + https://docs.gitlab.com/ce/api/project_level_variables.html
  + https://docs.gitlab.com/ce/api/group_level_variables.html

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

Builds/Jobs
===========

Builds/Jobs are associated to projects, pipelines and commits. They provide
information on the builds/jobs that have been run, and methods to manipulate
them.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectJob`
  + :class:`gitlab.v4.objects.ProjectJobManager`
  + :attr:`gitlab.v4.objects.Project.jobs`

* v3 API

  + :class:`gitlab.v3.objects.ProjectJob`
  + :class:`gitlab.v3.objects.ProjectJobManager`
  + :attr:`gitlab.v3.objects.Project.jobs`
  + :attr:`gitlab.Gitlab.project_jobs`

* GitLab API: https://docs.gitlab.com/ce/api/jobs.html

Examples
--------

Jobs are usually automatically triggered, but you can explicitly trigger a new
job:

Trigger a new job on a project:

.. literalinclude:: builds.py
   :start-after: # trigger run
   :end-before: # end trigger run

List jobs for the project:

.. literalinclude:: builds.py
   :start-after: # list
   :end-before: # end list

To list builds for a specific commit, create a
:class:`~gitlab.v3.objects.ProjectCommit` object and use its
:attr:`~gitlab.v3.objects.ProjectCommit.builds` method (v3 only):

.. literalinclude:: builds.py
   :start-after: # commit list
   :end-before: # end commit list

To list builds for a specific pipeline or get a single job within a specific
pipeline, create a
:class:`~gitlab.v4.objects.ProjectPipeline` object and use its
:attr:`~gitlab.v4.objects.ProjectPipeline.jobs` method (v4 only):

.. literalinclude:: builds.py
    :start-after: # pipeline list get
    :end-before: # end pipeline list get

Get a job:

.. literalinclude:: builds.py
   :start-after: # get job
   :end-before: # end get job

Get a job artifact:

.. literalinclude:: builds.py
   :start-after: # artifacts
   :end-before: # end artifacts

.. warning::

   Artifacts are entirely stored in memory in this example.

.. _streaming_example:

You can download artifacts as a stream. Provide a callable to handle the
stream:

.. literalinclude:: builds.py
   :start-after: # stream artifacts with class
   :end-before: # end stream artifacts with class

In this second example, you can directly stream the output into a file, and unzip it afterwards:

.. literalinclude:: builds.py
   :start-after: # stream artifacts with unzip
   :end-before: # end stream artifacts with unzip

Mark a job artifact as kept when expiration is set:

.. literalinclude:: builds.py
   :start-after: # keep artifacts
   :end-before: # end keep artifacts

Get a job trace:

.. literalinclude:: builds.py
   :start-after: # trace
   :end-before: # end trace

.. warning::

   Traces are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Cancel/retry a job:

.. literalinclude:: builds.py
   :start-after: # retry
   :end-before: # end retry

Play (trigger) a job:

.. literalinclude:: builds.py
   :start-after: # play
   :end-before: # end play

Erase a job (artifacts and trace):

.. literalinclude:: builds.py
   :start-after: # erase
   :end-before: # end erase

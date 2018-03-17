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

List triggers::

    triggers = project.triggers.list()

Get a trigger::

    trigger = project.triggers.get(trigger_token)

Create a trigger::

    trigger = project.triggers.create({}) # v3
    trigger = project.triggers.create({'description': 'mytrigger'}) # v4

Remove a trigger::

    project.triggers.delete(trigger_token)
    # or
    trigger.delete()

Full example with wait for finish::

    def get_or_create_trigger(project):
        trigger_decription = 'my_trigger_id'
        for t in project.triggers.list():
            if t.description == trigger_decription:
                return t
        return project.triggers.create({'description': trigger_decription})

    trigger = get_or_create_trigger(project)
    pipeline = project.trigger_pipeline('master', trigger.token, variables={"DEPLOY_ZONE": "us-west1"})
    while pipeline.finished_at is None:
        pipeline.refresh()
        os.sleep(1)

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

List variables::

    p_variables = project.variables.list()
    g_variables = group.variables.list()

Get a variable::

    p_var = project.variables.get('key_name')
    g_var = group.variables.get('key_name')

Create a variable::

    var = project.variables.create({'key': 'key1', 'value': 'value1'})
    var = group.variables.create({'key': 'key1', 'value': 'value1'})

Update a variable value::

    var.value = 'new_value'
    var.save()

Remove a variable::

    project.variables.delete('key_name')
    group.variables.delete('key_name')
    # or
    var.delete()

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
job::

    project.trigger_build('master', trigger_token,
                          {'extra_var1': 'foo', 'extra_var2': 'bar'})

List jobs for the project::

    builds = project.builds.list()  # v3
    jobs = project.jobs.list()  # v4

To list builds for a specific commit, create a
:class:`~gitlab.v3.objects.ProjectCommit` object and use its
:attr:`~gitlab.v3.objects.ProjectCommit.builds` method (v3 only)::

    # v3 only
    commit = gl.project_commits.get(commit_sha, project_id=1)
    builds = commit.builds()

To list builds for a specific pipeline or get a single job within a specific
pipeline, create a
:class:`~gitlab.v4.objects.ProjectPipeline` object and use its
:attr:`~gitlab.v4.objects.ProjectPipeline.jobs` method (v4 only)::

    # v4 only
    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    jobs = pipeline.jobs.list()  # gets all jobs in pipeline
    job = pipeline.jobs.get(job_id)  # gets one job from pipeline

Get a job::

    project.builds.get(build_id)  # v3
    project.jobs.get(job_id)  # v4

Get the artifacts of a job::

    build_or_job.artifacts()

.. warning::

   Artifacts are entirely stored in memory in this example.

.. _streaming_example:

You can download artifacts as a stream. Provide a callable to handle the
stream::

    class Foo(object):
        def __init__(self):
            self._fd = open('artifacts.zip', 'wb')

        def __call__(self, chunk):
            self._fd.write(chunk)

    target = Foo()
    build_or_job.artifacts(streamed=True, action=target)
    del(target)  # flushes data on disk

You can also directly stream the output into a file, and unzip it afterwards::

    zipfn = "___artifacts.zip"
    with open(zipfn, "wb") as f:
        build_or_job.artifacts(streamed=True, action=f.write)
    subprocess.run(["unzip", "-bo", zipfn])
    os.unlink(zipfn)

Get a single artifact file::

    build_or_job.artifact('path/to/file')

Mark a job artifact as kept when expiration is set::

    build_or_job.keep_artifacts()

Get a job trace::

    build_or_job.trace()

.. warning::

   Traces are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Cancel/retry a job::

    build_or_job.cancel()
    build_or_job.retry()

Play (trigger) a job::

    build_or_job.play()

Erase a job (artifacts and trace)::

    build_or_job.erase()

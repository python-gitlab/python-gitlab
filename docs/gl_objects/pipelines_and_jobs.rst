##################
Pipelines and Jobs
##################

Project pipelines
=================

A pipeline is a group of jobs executed by GitLab CI.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPipeline`
  + :class:`gitlab.v4.objects.ProjectPipelineManager`
  + :attr:`gitlab.v4.objects.Project.pipelines`

* GitLab API: https://docs.gitlab.com/ce/api/pipelines.html

Examples
--------

List pipelines for a project::

    pipelines = project.pipelines.list()

Get a pipeline for a project::

    pipeline = project.pipelines.get(pipeline_id)

Get variables of a pipeline::

    variables = pipeline.variables.list()

Create a pipeline for a particular reference with custom variables::

    pipeline = project.pipelines.create({'ref': 'master', 'variables': [{'key': 'MY_VARIABLE', 'value': 'hello'}]})

Retry the failed builds for a pipeline::

    pipeline.retry()

Cancel builds in a pipeline::

    pipeline.cancel()

Delete a pipeline::

    pipeline.delete()

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

* GitLab API: https://docs.gitlab.com/ce/api/pipeline_triggers.html

Examples
--------

List triggers::

    triggers = project.triggers.list()

Get a trigger::

    trigger = project.triggers.get(trigger_token)

Create a trigger::

    trigger = project.triggers.create({'description': 'mytrigger'})

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
        time.sleep(1)

You can trigger a pipeline using token authentication instead of user
authentication. To do so create an anonymous Gitlab instance and use lazy
objects to get the associated project::

    gl = gitlab.Gitlab(URL)  # no authentication
    project = gl.projects.get(project_id, lazy=True)  # no API call
    project.trigger_pipeline('master', trigger_token)

Reference: https://docs.gitlab.com/ee/ci/triggers/#trigger-token

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

List schedule variables::

    # note: you need to use get() to retrieve the schedule variables. The
    # attribute is not present in the response of a list() call
    sched = projects.pipelineschedules.get(schedule_id)
    vars = sched.attributes['variables']

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

Jobs
====

Jobs are associated to projects, pipelines and commits. They provide
information on the jobs that have been run, and methods to manipulate
them.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectJob`
  + :class:`gitlab.v4.objects.ProjectJobManager`
  + :attr:`gitlab.v4.objects.Project.jobs`

* GitLab API: https://docs.gitlab.com/ce/api/jobs.html

Examples
--------

Jobs are usually automatically triggered, but you can explicitly trigger a new
job::

    project.trigger_build('master', trigger_token,
                          {'extra_var1': 'foo', 'extra_var2': 'bar'})

List jobs for the project::

    jobs = project.jobs.list()

Get a single job::

    project.jobs.get(job_id)

List the jobs of a pipeline::

    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    jobs = pipeline.jobs.list()

.. note::

   Job methods (play, cancel, and so on) are not available on
   ``ProjectPipelineJob`` objects. To use these methods create a ``ProjectJob``
   object::

       pipeline_job = pipeline.jobs.list()[0]
       job = project.jobs.get(pipeline_job.id, lazy=True)
       job.retry()

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

Get a single artifact file by branch and job::

    project.artifact('branch', 'path/to/file', 'job')

Mark a job artifact as kept when expiration is set::

    build_or_job.keep_artifacts()

Delete the artifacts of a job::

    build_or_job.delete_artifacts()

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

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

    pipeline = project.pipelines.create({'ref': 'main', 'variables': [{'key': 'MY_VARIABLE', 'value': 'hello'}]})

Retry the failed builds for a pipeline::

    pipeline.retry()

Cancel builds in a pipeline::

    pipeline.cancel()

Delete a pipeline::

    pipeline.delete()

Get latest pipeline::

    project.pipelines.latest(ref="main")


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
    pipeline = project.trigger_pipeline('main', trigger.token, variables={"DEPLOY_ZONE": "us-west1"})
    while pipeline.finished_at is None:
        pipeline.refresh()
        time.sleep(1)

You can trigger a pipeline using token authentication instead of user
authentication. To do so create an anonymous Gitlab instance and use lazy
objects to get the associated project::

    gl = gitlab.Gitlab(URL)  # no authentication
    project = gl.projects.get(project_id, lazy=True)  # no API call
    project.trigger_pipeline('main', trigger_token)

Reference: https://docs.gitlab.com/ee/ci/triggers/#trigger-token

Pipeline schedules
==================

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
  + :attr:`gitlab.v4.objects.ProjectPipelineSchedule.variables`
  + :class:`gitlab.v4.objects.ProjectPipelineSchedulePipeline`
  + :class:`gitlab.v4.objects.ProjectPipelineSchedulePipelineManager`
  + :attr:`gitlab.v4.objects.ProjectPipelineSchedule.pipelines`

* GitLab API: https://docs.gitlab.com/ce/api/pipeline_schedules.html

Examples
--------

List pipeline schedules::

    scheds = project.pipelineschedules.list()

Get a single schedule::

    sched = project.pipelineschedules.get(schedule_id)

Create a new schedule::

    sched = project.pipelineschedules.create({
        'ref': 'main',
        'description': 'Daily test',
        'cron': '0 1 * * *'})

Update a schedule::

    sched.cron = '1 2 * * *'
    sched.save()

Take ownership of a schedule:

    sched.take_ownership()

Trigger a pipeline schedule immediately::

    sched = projects.pipelineschedules.get(schedule_id)
    sched.play()

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

List all pipelines triggered by a pipeline schedule::

    pipelines = sched.pipelines.list()

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

    project.trigger_build('main', trigger_token,
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

Get the artifacts of a job by its name from the latest successful pipeline of
a branch or tag::

  project.artifacts.download(ref_name='main', job='build')

.. warning::

   Artifacts are entirely stored in memory in this example.

.. _streaming_example:

You can download artifacts as a stream. Provide a callable to handle the
stream::

    with open("archive.zip", "wb") as f:
         build_or_job.artifacts(streamed=True, action=f.write)

You can also directly stream the output into a file, and unzip it afterwards::

    zipfn = "___artifacts.zip"
    with open(zipfn, "wb") as f:
        build_or_job.artifacts(streamed=True, action=f.write)
    subprocess.run(["unzip", "-bo", zipfn])
    os.unlink(zipfn)

Or, you can also use the underlying response iterator directly::

    artifact_bytes_iterator = build_or_job.artifacts(iterator=True)

This can be used with frameworks that expect an iterator (such as FastAPI/Starlette's
``StreamingResponse``) to forward a download from GitLab without having to download
the entire content server-side first::

    @app.get("/download_artifact")
    def download_artifact():
        artifact_bytes_iterator = build_or_job.artifacts(iterator=True)
        return StreamingResponse(artifact_bytes_iterator, media_type="application/zip")

Delete all artifacts of a project that can be deleted::

  project.artifacts.delete()

Get a single artifact file::

    build_or_job.artifact('path/to/file')

Get a single artifact file by branch and job::

    project.artifacts.raw('branch', 'path/to/file', 'job')

Mark a job artifact as kept when expiration is set::

    build_or_job.keep_artifacts()

Delete the artifacts of a job::

    build_or_job.delete_artifacts()

Get a job log file / trace::

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


Pipeline bridges
=====================

Get a list of bridge jobs (including child pipelines) for a pipeline.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectPipelineBridge`
  + :class:`gitlab.v4.objects.ProjectPipelineBridgeManager`
  + :attr:`gitlab.v4.objects.ProjectPipeline.bridges`

* GitLab API: https://docs.gitlab.com/ee/api/jobs.html#list-pipeline-bridges

Examples
--------

List bridges for the pipeline::

    bridges = pipeline.bridges.list()

Pipeline test report
====================

Get a pipeline's complete test report.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectPipelineTestReport`
  + :class:`gitlab.v4.objects.ProjectPipelineTestReportManager`
  + :attr:`gitlab.v4.objects.ProjectPipeline.test_report`

* GitLab API: https://docs.gitlab.com/ee/api/pipelines.html#get-a-pipelines-test-report

Examples
--------

Get the test report for a pipeline::

    test_report = pipeline.test_report.get()

Pipeline test report summary
============================

Get a pipeline’s test report summary.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectPipelineTestReportSummary`
  + :class:`gitlab.v4.objects.ProjectPipelineTestReportSummaryManager`
  + :attr:`gitlab.v4.objects.ProjectPipeline.test_report_summary`

* GitLab API: https://docs.gitlab.com/ee/api/pipelines.html#get-a-pipelines-test-report-summary

Examples
--------

Get the test report summary for a pipeline::

    test_report_summary = pipeline.test_report_summary.get()


#######
Runners
#######

Runners are external processes used to run CI jobs. They are deployed by the
administrator and registered to the GitLab instance.

Shared runners are available for all projects. Specific runners are enabled for
a list of projects.

Global runners (admin)
======================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Runner`
  + :class:`gitlab.v4.objects.RunnerManager`
  + :attr:`gitlab.Gitlab.runners`

* GitLab API: https://docs.gitlab.com/ce/api/runners.html

Examples
--------

Use the ``list()`` and ``all()`` methods to list runners.

Both methods accept a ``scope`` parameter to filter the list. Allowed values
for this parameter are:

* ``active``
* ``paused``
* ``online``
* ``specific`` (``all()`` only)
* ``shared`` (``all()`` only)

.. note::

   The returned objects hold minimal information about the runners. Use the
   ``get()`` method to retrieve detail about a runner.

::

    # List owned runners
    runners = gl.runners.list()
    # With a filter
    runners = gl.runners.list(scope='active')
    # List all runners, using a filter
    runners = gl.runners.all(scope='paused')

Get a runner's detail::

    runner = gl.runners.get(runner_id)

Update a runner::

    runner = gl.runners.get(runner_id)
    runner.tag_list.append('new_tag')
    runner.save()

Remove a runner::

    gl.runners.delete(runner_id)
    # or
    runner.delete()

Project runners
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRunner`
  + :class:`gitlab.v4.objects.ProjectRunnerManager`
  + :attr:`gitlab.v4.objects.Project.runners`

* GitLab API: https://docs.gitlab.com/ce/api/runners.html

Examples
--------

List the runners for a project::

    runners = project.runners.list()

Enable a specific runner for a project::

    p_runner = project.runners.create({'runner_id': runner.id})

Disable a specific runner for a project::

    project.runners.delete(runner.id)

Runner jobs
===========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.RunnerJob`
  + :class:`gitlab.v4.objects.RunnerJobManager`
  + :attr:`gitlab.v4.objects.Runner.jobs`

* GitLab API: https://docs.gitlab.com/ce/api/runners.html

Examples
--------

List for jobs for a runner::

    jobs = runner.jobs.list()

Filter the list using the jobs status::

    # status can be 'running', 'success', 'failed' or 'canceled'
    active_jobs = runner.jobs.list(status='running')

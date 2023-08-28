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
  + :class:`gitlab.v4.objects.RunnerAll`
  + :class:`gitlab.v4.objects.RunnerAllManager`
  + :attr:`gitlab.Gitlab.runners_all`

* GitLab API: https://docs.gitlab.com/ce/api/runners.html

Examples
--------

Use the ``runners.list()`` and ``runners_all.list()`` methods to list runners.
``runners.list()`` - Get a list of specific runners available to the user
``runners_all.list()``  - Get a list of all runners in the GitLab instance 
(specific and shared). Access is restricted to users with administrator access.


Both methods accept a ``scope`` parameter to filter the list. Allowed values
for this parameter are:

* ``active``
* ``paused``
* ``online``
* ``specific`` (``runners_all.list()`` only)
* ``shared`` (``runners_all.list()`` only)

.. note::

   The returned objects hold minimal information about the runners. Use the
   ``get()`` method to retrieve detail about a runner.

   Runners returned via ``runners_all.list()`` also cannot be manipulated
   directly. You will need to use the ``get()`` method to create an editable
   object.

::

    # List owned runners
    runners = gl.runners.list()

    # List owned runners with a filter
    runners = gl.runners.list(scope='active')

    # List all runners in the GitLab instance (specific and shared), using a filter
    runners = gl.runners_all.list(scope='paused')

Get a runner's detail::

    runner = gl.runners.get(runner_id)

Register a new runner::

    runner = gl.runners.create({'token': secret_token})

.. note::

   A new runner registration workflow has been introduced since GitLab 16.0. This new
   workflow comes with a new API endpoint to create runners, which does not use
   registration tokens.

   The new endpoint can be called using ``gl.user.runners.create()`` after
   authenticating with ``gl.auth()``.

Update a runner::

    runner = gl.runners.get(runner_id)
    runner.tag_list.append('new_tag')
    runner.save()

Remove a runner::

    gl.runners.delete(runner_id)
    # or
    runner.delete()

Remove a runner by its authentication token::

    gl.runners.delete(token="runner-auth-token")

Verify a registered runner token::

    try:
        gl.runners.verify(runner_token)
        print("Valid token")
    except GitlabVerifyError:
        print("Invalid token")

Project/Group runners
=====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRunner`
  + :class:`gitlab.v4.objects.ProjectRunnerManager`
  + :attr:`gitlab.v4.objects.Project.runners`
  + :class:`gitlab.v4.objects.GroupRunner`
  + :class:`gitlab.v4.objects.GroupRunnerManager`
  + :attr:`gitlab.v4.objects.Group.runners`

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

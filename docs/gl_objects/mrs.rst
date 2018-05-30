##############
Merge requests
##############

You can use merge requests to notify a project that a branch is ready for
merging. The owner of the target projet can accept the merge request.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeRequest`
  + :class:`gitlab.v4.objects.ProjectMergeRequestManager`
  + :attr:`gitlab.v4.objects.Project.mergerequests`

* GitLab API: https://docs.gitlab.com/ce/api/merge_requests.html

Examples
--------

List MRs for a project::

    mrs = project.mergerequests.list()

You can filter and sort the returned list with the following parameters:

* ``state``: state of the MR. It can be one of ``all``, ``merged``, ``opened``
  or ``closed``
* ``order_by``: sort by ``created_at`` or ``updated_at``
* ``sort``: sort order (``asc`` or ``desc``)

For example::

    mrs = project.mergerequests.list(state='merged', order_by='updated_at')

Get a single MR::

    mr = project.mergerequests.get(mr_id)

Create a MR::

    mr = project.mergerequests.create({'source_branch': 'cool_feature',
                                       'target_branch': 'master',
                                       'title': 'merge cool feature',
                                       'labels': ['label1', 'label2']})

Update a MR::

    mr.description = 'New description'
    mr.labels = ['foo', 'bar']
    mr.save()

Change the state of a MR (close or reopen)::

    mr.state_event = 'close'  # or 'reopen'
    mr.save()

Delete a MR::

    project.mergerequests.delete(mr_id)
    # or
    mr.delete()

Accept a MR::

    mr.merge()

Cancel a MR when the build succeeds::

    mr.cancel_merge_when_pipeline_succeeds()

List commits of a MR::

    commits = mr.commits()

List issues that will close on merge::

    mr.closes_issues()

Subscribe to / unsubscribe from a MR::

    mr.subscribe()
    mr.unsubscribe()

Mark a MR as todo::

    mr.todo()

List the diffs for a merge request::

    diffs = mr.diffs.list()

Get a diff for a merge request::

    diff = mr.diffs.get(diff_id)

Get time tracking stats::

    merge request.time_stats()

On recent versions of Gitlab the time stats are also returned as a merge
request object attribute::

    mr = project.mergerequests.get(id)
    print(mr.attributes['time_stats'])

Set a time estimate for a merge request::

    mr.time_estimate('3h30m')

Reset a time estimate for a merge request::

    mr.reset_time_estimate()

Add spent time for a merge request::

    mr.add_spent_time('3h30m')

Reset spent time for a merge request::

    mr.reset_spent_time()

Get user agent detail for the issue (admin only)::

    detail = issue.user_agent_detail()

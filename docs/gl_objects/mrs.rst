##############
Merge requests
##############

You can use merge requests to notify a project that a branch is ready for
merging. The owner of the target projet can accept the merge request.

The v3 API uses the ``id`` attribute to identify a merge request, the v4 API
uses the ``iid`` attribute.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeRequest`
  + :class:`gitlab.v4.objects.ProjectMergeRequestManager`
  + :attr:`gitlab.v4.objects.Project.mergerequests`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectMergeRequest`
  + :class:`gitlab.v3.objects.ProjectMergeRequestManager`
  + :attr:`gitlab.v3.objects.Project.mergerequests`
  + :attr:`gitlab.Gitlab.project_mergerequests`

* GitLab API: https://docs.gitlab.com/ce/api/merge_requests.html

Examples
--------

List MRs for a project::

    mrs = project.mergerequests.list()

You can filter and sort the returned list with the following parameters:

* ``iid``: iid (unique ID for the project) of the MR (v3 API)
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

    mr.cancel_merge_when_build_succeeds()  # v3
    mr.cancel_merge_when_pipeline_succeeds()  # v4

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

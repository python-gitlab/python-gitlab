.. _merge_requests_examples:

##############
Merge requests
##############

You can use merge requests to notify a project that a branch is ready for
merging. The owner of the target projet can accept the merge request.

Merge requests are linked to projects, but they can be listed globally or for
groups.

Group and global listing
========================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupMergeRequest`
  + :class:`gitlab.v4.objects.GroupMergeRequestManager`
  + :attr:`gitlab.v4.objects.Group.mergerequests`
  + :class:`gitlab.v4.objects.MergeRequest`
  + :class:`gitlab.v4.objects.MergeRequestManager`
  + :attr:`gitlab.Gitlab.mergerequests`

* GitLab API: https://docs.gitlab.com/ce/api/merge_requests.html

Examples
--------

List the merge requests created by the user of the token on the GitLab server::

    mrs = gl.mergerequests.list()

List the merge requests available on the GitLab server::

    mrs = gl.mergerequests.list(scope="all")

List the merge requests for a group::

    group = gl.groups.get('mygroup')
    mrs = group.mergerequests.list()

.. note::

   It is not possible to edit or delete ``MergeRequest`` and
   ``GroupMergeRequest`` objects. You need to create a ``ProjectMergeRequest``
   object to apply changes::

       mr = group.mergerequests.list()[0]
       project = gl.projects.get(mr.project_id, lazy=True)
       editable_mr = project.mergerequests.get(mr.iid, lazy=True)
       editable_mr.title = updated_title
       editable_mr.save()

Project merge requests
======================

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

* ``state``: state of the MR. It can be one of ``all``, ``merged``, ``opened``,
   ``closed`` or ``locked``
* ``order_by``: sort by ``created_at`` or ``updated_at``
* ``sort``: sort order (``asc`` or ``desc``)

You can find a full updated list of parameters here:
https://docs.gitlab.com/ee/api/merge_requests.html#list-merge-requests

For example::

    mrs = project.mergerequests.list(state='merged', order_by='updated_at')

Get a single MR::

    mr = project.mergerequests.get(mr_iid)

Get MR reviewer details::

    mr = project.mergerequests.get(mr_iid)
    reviewers = mr.reviewer_details.list()

Create a MR::

    mr = project.mergerequests.create({'source_branch': 'cool_feature',
                                       'target_branch': 'main',
                                       'title': 'merge cool feature',
                                       'labels': ['label1', 'label2']})

    # Use a project MR description template
    mr_description_template = project.merge_request_templates.get("Default")
    mr = project.mergerequests.create({'source_branch': 'cool_feature',
                                       'target_branch': 'main',
                                       'title': 'merge cool feature',
                                       'description': mr_description_template.content})

Update a MR::

    mr.description = 'New description'
    mr.labels = ['foo', 'bar']
    mr.save()

Change the state of a MR (close or reopen)::

    mr.state_event = 'close'  # or 'reopen'
    mr.save()

Delete a MR::

    project.mergerequests.delete(mr_iid)
    # or
    mr.delete()

Accept a MR::

    mr.merge()

Schedule a MR to merge after the pipeline(s) succeed::

    mr.merge(merge_when_pipeline_succeeds=True)

Cancel a MR from merging when the pipeline succeeds::

    # Cancel a MR from being merged that had been previously set to
    # 'merge_when_pipeline_succeeds=True'
    mr.cancel_merge_when_pipeline_succeeds()

List commits of a MR::

    commits = mr.commits()

List the changes of a MR::

    changes = mr.changes()

List issues related to this merge request::

    related_issues = mr.related_issues()

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

    time_stats = mr.time_stats()

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

Attempt to rebase an MR::

    mr.rebase()

Clear all approvals of a merge request (possible with project or group access tokens only)::

    mr.reset_approvals()

Get status of a rebase for an MR::

    mr = project.mergerequests.get(mr_id, include_rebase_in_progress=True)
    print(mr.rebase_in_progress, mr.merge_error)

For more info see:
https://docs.gitlab.com/ee/api/merge_requests.html#rebase-a-merge-request

Attempt to merge changes between source and target branch::

    response = mr.merge_ref()
    print(response['commit_id'])

Merge Request Pipelines
=======================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeRequestPipeline`
  + :class:`gitlab.v4.objects.ProjectMergeRequestPipelineManager`
  + :attr:`gitlab.v4.objects.ProjectMergeRequest.pipelines`

* GitLab API: https://docs.gitlab.com/ee/api/merge_requests.html#list-mr-pipelines

Examples
--------

List pipelines for a merge request::

    pipelines = mr.pipelines.list()

Create a pipeline for a merge request::

    pipeline = mr.pipelines.create()

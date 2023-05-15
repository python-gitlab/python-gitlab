.. _issues_examples:

######
Issues
######

Reported issues
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Issue`
  + :class:`gitlab.v4.objects.IssueManager`
  + :attr:`gitlab.Gitlab.issues`

* GitLab API: https://docs.gitlab.com/ce/api/issues.html

Examples
--------

List the issues::

    issues = gl.issues.list()

Use the ``state`` and ``label`` parameters to filter the results. Use the
``order_by`` and ``sort`` attributes to sort the results::

    open_issues = gl.issues.list(state='opened')
    closed_issues = gl.issues.list(state='closed')
    tagged_issues = gl.issues.list(labels=['foo', 'bar'])

.. note::

   It is not possible to edit or delete Issue objects. You need to create a
   ProjectIssue object to perform changes::

       issue = gl.issues.list()[0]
       project = gl.projects.get(issue.project_id, lazy=True)
       editable_issue = project.issues.get(issue.iid, lazy=True)
       editable_issue.title = updated_title
       editable_issue.save()

Group issues
============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupIssue`
  + :class:`gitlab.v4.objects.GroupIssueManager`
  + :attr:`gitlab.v4.objects.Group.issues`

* GitLab API: https://docs.gitlab.com/ce/api/issues.html

Examples
--------

List the group issues::

    issues = group.issues.list()
    # Filter using the state, labels and milestone parameters
    issues = group.issues.list(milestone='1.0', state='opened')
    # Order using the order_by and sort parameters
    issues = group.issues.list(order_by='created_at', sort='desc')

.. note::

   It is not possible to edit or delete GroupIssue objects. You need to create
   a ProjectIssue object to perform changes::

       issue = group.issues.list()[0]
       project = gl.projects.get(issue.project_id, lazy=True)
       editable_issue = project.issues.get(issue.iid, lazy=True)
       editable_issue.title = updated_title
       editable_issue.save()

Project issues
==============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssue`
  + :class:`gitlab.v4.objects.ProjectIssueManager`
  + :attr:`gitlab.v4.objects.Project.issues`

* GitLab API: https://docs.gitlab.com/ce/api/issues.html

Examples
--------

List the project issues::

    issues = project.issues.list()
    # Filter using the state, labels and milestone parameters
    issues = project.issues.list(milestone='1.0', state='opened')
    # Order using the order_by and sort parameters
    issues = project.issues.list(order_by='created_at', sort='desc')

Get a project issue::

    issue = project.issues.get(issue_iid)

Create a new issue::

    issue = project.issues.create({'title': 'I have a bug',
                                   'description': 'Something useful here.'})

Update an issue::

    issue.labels = ['foo', 'bar']
    issue.save()

Close / reopen an issue::

    # close an issue
    issue.state_event = 'close'
    issue.save()
    # reopen it
    issue.state_event = 'reopen'
    issue.save()

Delete an issue (admin or project owner only)::

    project.issues.delete(issue_id)
    # or
    issue.delete()


Assign the issues::

    issue = gl.issues.list()[0]
    issue.assignee_ids = [25, 10, 31, 12]
    issue.save()

.. note::
    The Gitlab API explicitly references that the `assignee_id` field is deprecated,
    so using a list of user IDs for `assignee_ids` is how to assign an issue to a user(s).

Subscribe / unsubscribe from an issue::

    issue.subscribe()
    issue.unsubscribe()

Move an issue to another project::

    issue.move(other_project_id)

Reorder an issue on a board::

    issue.reorder(move_after_id=2, move_before_id=3)

Make an issue as todo::

    issue.todo()

Get time tracking stats::

    issue.time_stats()

On recent versions of Gitlab the time stats are also returned as an issue
object attribute::

    issue = project.issue.get(iid)
    print(issue.attributes['time_stats'])

Set a time estimate for an issue::

    issue.time_estimate('3h30m')

Reset a time estimate for an issue::

    issue.reset_time_estimate()

Add spent time for an issue::

    issue.add_spent_time('3h30m')

Reset spent time for an issue::

    issue.reset_spent_time()

Get user agent detail for the issue (admin only)::

    detail = issue.user_agent_detail()

Get the list of merge requests that will close an issue when merged::

    mrs = issue.closed_by()

Get the merge requests related to an issue::

    mrs = issue.related_merge_requests()

Get the list of participants::

    users = issue.participants()

Get the list of iteration events::

    iteration_events = issue.resource_iteration_events.list()

Get the list of weight events::

    weight_events = issue.resource_weight_events.list()

Issue links
===========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssueLink`
  + :class:`gitlab.v4.objects.ProjectIssueLinkManager`
  + :attr:`gitlab.v4.objects.ProjectIssue.links`

* GitLab API: https://docs.gitlab.com/ee/api/issue_links.html

Examples
--------

List the issues linked to ``i1``::

    links = i1.links.list()

Link issue ``i1`` to issue ``i2``::

    data = {
        'target_project_id': i2.project_id,
        'target_issue_iid': i2.iid
    }
    src_issue, dest_issue = i1.links.create(data)

.. note::

   The ``create()`` method returns the source and destination ``ProjectIssue``
   objects, not a ``ProjectIssueLink`` object.

Delete a link::

    i1.links.delete(issue_link_id)

Issues statistics
=========================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.IssuesStatistics`
  + :class:`gitlab.v4.objects.IssuesStatisticsManager`
  + :attr:`gitlab.issues_statistics`
  + :class:`gitlab.v4.objects.GroupIssuesStatistics`
  + :class:`gitlab.v4.objects.GroupIssuesStatisticsManager`
  + :attr:`gitlab.v4.objects.Group.issues_statistics`
  + :class:`gitlab.v4.objects.ProjectIssuesStatistics`
  + :class:`gitlab.v4.objects.ProjectIssuesStatisticsManager`
  + :attr:`gitlab.v4.objects.Project.issues_statistics`


* GitLab API: https://docs.gitlab.com/ce/api/issues_statistics.htm

Examples
---------

Get statistics of all issues created by the current user::

    statistics = gl.issues_statistics.get()

Get statistics of all issues the user has access to::

    statistics = gl.issues_statistics.get(scope='all')

Get statistics of issues for the user with ``foobar`` in the ``title`` or the ``description``::

    statistics = gl.issues_statistics.get(search='foobar')

Get statistics of all issues in a group::

    statistics = group.issues_statistics.get()

Get statistics of issues in a group with ``foobar`` in the ``title`` or the ``description``::

    statistics = group.issues_statistics.get(search='foobar')

Get statistics of all issues in a project::

    statistics = project.issues_statistics.get()

Get statistics of issues in a project with ``foobar`` in the ``title`` or the ``description``::

    statistics = project.issues_statistics.get(search='foobar')

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

Delete an issue::

    project.issues.delete(issue_id)
    # pr
    issue.delete()

Subscribe / unsubscribe from an issue::

    issue.subscribe()
    issue.unsubscribe()

Move an issue to another project::

    issue.move(other_project_id)

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

Get the list of participants::

    users = issue.participants()

Issue links
===========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIssueLink`
  + :class:`gitlab.v4.objects.ProjectIssueLinkManager`
  + :attr:`gitlab.v4.objects.ProjectIssue.links`

* GitLab API: https://docs.gitlab.com/ee/api/issue_links.html (EE feature)

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

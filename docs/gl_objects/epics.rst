#####
Epics
#####

Epics
=====

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupEpic`
  + :class:`gitlab.v4.objects.GroupEpicManager`
  + :attr:`gitlab.Gitlab.Group.epics`

* GitLab API: https://docs.gitlab.com/ee/api/epics.html (EE feature)

Examples
--------

List the epics for a group::

    epics = groups.epics.list()

Get a single epic for a group::

    epic = group.epics.get(epic_iid)

Create an epic for a group::

    epic = group.epics.create({'title': 'My Epic'})

Edit an epic::

    epic.title = 'New title'
    epic.labels = ['label1', 'label2']
    epic.save()

Delete an epic::

    epic.delete()

Epics issues
============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupEpicIssue`
  + :class:`gitlab.v4.objects.GroupEpicIssueManager`
  + :attr:`gitlab.Gitlab.GroupEpic.issues`

* GitLab API: https://docs.gitlab.com/ee/api/epic_issues.html (EE feature)

Examples
--------

List the issues associated with an issue::

    ei = epic.issues.list()

Associate an issue with an epic::

    # use the issue id, not its iid
    ei = epic.issues.create({'issue_id': 4})

Move an issue in the list::

    ei.move_before_id = epic_issue_id_1
    # or
    ei.move_after_id = epic_issue_id_2
    ei.save()

Delete an issue association::

    ei.delete()

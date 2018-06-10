############
Issue boards
############

Boards
======

Boards are a visual representation of existing issues for a project or a group.
Issues can be moved from one list to the other to track progress and help with
priorities.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectBoard`
  + :class:`gitlab.v4.objects.ProjectBoardManager`
  + :attr:`gitlab.v4.objects.Project.boards`
  + :class:`gitlab.v4.objects.GroupBoard`
  + :class:`gitlab.v4.objects.GroupBoardManager`
  + :attr:`gitlab.v4.objects.Group.boards`

* GitLab API:

  + https://docs.gitlab.com/ce/api/boards.html
  + https://docs.gitlab.com/ce/api/group_boards.html

Examples
--------

Get the list of existing boards for a project or a group::

    # item is a Project or a Group
    boards = project_or_group.boards.list()

Get a single board for a project or a group::

    board = project_or_group.boards.get(board_id)

Create a board::

    board = project_or_group.boards.create({'name': 'new-board'})

.. note:: Board creation is not supported in the GitLab CE edition.

Delete a board::

    board.delete()
    # or
    project_or_group.boards.delete(board_id)

.. note:: Board deletion is not supported in the GitLab CE edition.

Board lists
===========

Boards are made of lists of issues. Each list is associated to a label, and
issues tagged with this label automatically belong to the list.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectBoardList`
  + :class:`gitlab.v4.objects.ProjectBoardListManager`
  + :attr:`gitlab.v4.objects.ProjectBoard.lists`
  + :class:`gitlab.v4.objects.GroupBoardList`
  + :class:`gitlab.v4.objects.GroupBoardListManager`
  + :attr:`gitlab.v4.objects.GroupBoard.lists`

* GitLab API:

  + https://docs.gitlab.com/ce/api/boards.html
  + https://docs.gitlab.com/ce/api/group_boards.html

Examples
--------

List the issue lists for a board::

    b_lists = board.lists.list()

Get a single list::

    b_list = board.lists.get(list_id)

Create a new list::

    # First get a ProjectLabel
    label = get_or_create_label()
    # Then use its ID to create the new board list
    b_list = board.lists.create({'label_id': label.id})

Change a list position. The first list is at position 0. Moving a list will
set it at the given position and move the following lists up a position::

    b_list.position = 2
    b_list.save()

Delete a list::

    b_list.delete()

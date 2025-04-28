#####
Todos
#####

Reference
---------

* v4 API:

  + :class:`~gitlab.objects.Todo`
  + :class:`~gitlab.objects.TodoManager`
  + :attr:`gitlab.Gitlab.todos`

* GitLab API: https://docs.gitlab.com/api/todos

Examples
--------

List active todos::

    todos = gl.todos.list(get_all=True)

You can filter the list using the following parameters:

* ``action``: can be ``assigned``, ``mentioned``, ``build_failed``, ``marked``,
  or ``approval_required``
* ``author_id``
* ``project_id``
* ``state``: can be ``pending`` or ``done``
* ``type``: can be ``Issue`` or ``MergeRequest``

For example::

    todos = gl.todos.list(project_id=1, get_all=True)
    todos = gl.todos.list(state='done', type='Issue', get_all=True)

Mark a todo as done::

    todos = gl.todos.list(project_id=1, get_all=True)
    todos[0].mark_as_done()

Mark all the todos as done::

    gl.todos.mark_all_as_done()

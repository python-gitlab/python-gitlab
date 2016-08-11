# list
todos = gl.todos.list()
# end list

# filter
todos = gl.todos.list(project_id=1)
todos = gl.todos.list(state='done', type='Issue')
# end filter

# get
todo = gl.todos.get(todo_id)
# end get

# delete
gl.todos.delete(todo_id)
# or
todo.delete()
# end delete

# all_delete
nb_of_closed_todos = gl.todos.delete_all()
# end all_delete

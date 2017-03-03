# list
issues = gl.issues.list()
# end list

# filtered list
open_issues = gl.issues.list(state='opened')
closed_issues = gl.issues.list(state='closed')
tagged_issues = gl.issues.list(labels=['foo', 'bar'])
# end filtered list

# group issues list
issues = gl.group_issues.list(group_id=1)
# or
issues = group.issues.list()
# Filter using the state, labels and milestone parameters
issues = group.issues.list(milestone='1.0', state='opened')
# Order using the order_by and sort parameters
issues = group.issues.list(order_by='created_at', sort='desc')
# end group issues list

# project issues list
issues = gl.project_issues.list(project_id=1)
# or
issues = project.issues.list()
# Filter using the state, labels and milestone parameters
issues = project.issues.list(milestone='1.0', state='opened')
# Order using the order_by and sort parameters
issues = project.issues.list(order_by='created_at', sort='desc')
# end project issues list

# project issues get
issue = gl.project_issues.get(issue_id, project_id=1)
# or
issue = project.issues.get(issue_id)
# end project issues get

# project issues create
issue = gl.project_issues.create({'title': 'I have a bug',
                                  'description': 'Something useful here.'},
                                 project_id=1)
# or
issue = project.issues.create({'title': 'I have a bug',
                               'description': 'Something useful here.'})
# end project issues create

# project issue update
issue.labels = ['foo', 'bar']
issue.save()
# end project issue update

# project issue open_close
# close an issue
issue.state_event = 'close'
issue.save()
# reopen it
issue.state_event = 'reopen'
issue.save()
# end project issue open_close

# project issue delete
gl.project_issues.delete(issue_id, project_id=1)
# or
project.issues.delete(issue_id)
# pr
issue.delete()
# end project issue delete

# project issue subscribe
issue.subscribe()
issue.unsubscribe()
# end project issue subscribe

# project issue move
issue.move(new_project_id)
# end project issue move

# project issue todo
issue.todo()
# end project issue todo

# project issue time tracking stats
issue.time_stats()
# end project issue time tracking stats

# project issue set time estimate
issue.set_time_estimate({'duration': '3h30m'})
# end project issue set time estimate

# project issue reset time estimate
issue.reset_time_estimate()
# end project issue reset time estimate

# project issue set time spent
issue.add_time_spent({'duration': '3h30m'})
# end project issue set time spent

# project issue reset time spent
issue.reset_time_spent()
# end project issue reset time spent

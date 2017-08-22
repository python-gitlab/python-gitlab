# list
# List owned runners
runners = gl.runners.list()
# With a filter
runners = gl.runners.list(scope='active')
# List all runners, using a filter
runners = gl.runners.all(scope='paused')
# end list

# get
runner = gl.runners.get(runner_id)
# end get

# update
runner = gl.runners.get(runner_id)
runner.tag_list.append('new_tag')
runner.save()
# end update

# delete
gl.runners.delete(runner_id)
# or
runner.delete()
# end delete

# project list
runners = project.runners.list()
# end project list

# project enable
p_runner = project.runners.create({'runner_id': runner.id})
# end project enable

# project disable
project.runners.delete(runner.id)
# end project disable

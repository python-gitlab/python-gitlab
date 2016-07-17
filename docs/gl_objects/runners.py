# list
# List owned runners
runners = gl.runners.list()
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

# list
hooks = gl.hooks.list()
# end list

# test
gl.hooks.get(hook_id)
# end test

# create
hook = gl.hooks.create({'url': 'http://your.target.url'})
# end create

# delete
gl.hooks.delete(hook_id)
# or
hook.delete()
# end delete

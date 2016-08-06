# global list
keys = gl.keys.list()
# end global list

# global get
key = gl.keys.get(key_id)
# end global key

# list
keys = gl.project_keys.list(project_id=1)
# or
keys = project.keys.list()
# end list

# get
key = gl.project_keys.get(key_id, project_id=1)
# or
key = project.keys.get(key_id)
# end get

# create
key = gl.project_keys.create({'title': 'jenkins key',
                              'key': open('/home/me/.ssh/id_rsa.pub').read()},
                             project_id=1)
# or
key = project.keys.create({'title': 'jenkins key',
                           'key': open('/home/me/.ssh/id_rsa.pub').read()})
# end create

# delete
key = gl.project_keys.delete(key_id, project_id=1)
# or
key = project.keys.list(key_id)
# or
key.delete()
# end delete

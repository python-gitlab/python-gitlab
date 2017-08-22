# global list
keys = gl.deploykeys.list()
# end global list

# global get
key = gl.deploykeys.get(key_id)
# end global get

# list
keys = project.keys.list()
# end list

# get
key = project.keys.get(key_id)
# end get

# create
key = project.keys.create({'title': 'jenkins key',
                           'key': open('/home/me/.ssh/id_rsa.pub').read()})
# end create

# delete
key = project.keys.list(key_id)
# or
key.delete()
# end delete

# enable
project.keys.enable(key_id)
# end enable

# disable
project_key.delete()  # v4
project.keys.disable(key_id)  # v3
# end disable

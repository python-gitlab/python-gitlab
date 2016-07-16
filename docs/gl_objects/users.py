# list
users = gl.users.list()
# end list

# search
users = gl.users.list(search='oo')
# end search

# get
# by ID
user = gl.users.get(2)
# by username
user = gl.users.list(username='root')
# end get

# create
user = gl.users.create({'email': 'john@doe.com',
                        'password': 's3cur3s3cr3T',
                        'username': 'jdoe',
                        'name': 'John Doe'})
# end create

# update
user.name = 'Real Name'
user.save()
# end update

# delete
gl.users.delete(2)
user.delete()
# end delete

# block
user.block()
user.unblock()
# end block

# key list
keys = gl.user_keys.list(user_id=1)
# or
keys = user.keys.list()
# end key list

# key get
key = gl.user_keys.list(1, user_id=1)
# or
key = user.keys.get(1)
# end key get

# key create
k = gl.user_keys.create({'title': 'my_key',
                         'key': open('/home/me/.ssh/id_rsa.pub').read()},
                        user_id=2)
# or
k = user.keys.create({'title': 'my_key',
                      'key': open('/home/me/.ssh/id_rsa.pub').read()})
# end key create

# key delete
gl.user_keys.delete(1, user_id=1)
# or
user.keys.delete(1)
# or
key.delete()
# end key delete

# currentuser get
gl.auth()
current_user = gl.user
# end currentuser get

# currentuser key list
keys = gl.user.keys.list()
# end currentuser key list

# currentuser key get
key = gl.user.keys.get(1)
# end currentuser key get

# currentuser key create
key = gl.user.keys.create({'id': 'my_key', 'key': key_content})
# end currentuser key create

# currentuser key delete
gl.user.keys.delete(1)
# or
key.delete()
# end currentuser key delete

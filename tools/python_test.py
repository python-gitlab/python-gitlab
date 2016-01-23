import base64

import gitlab

LOGIN = 'root'
PASSWORD = '5iveL!fe'

SSH_KEY = ("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZAjAX8vTiHD7Yi3/EzuVaDChtih"
           "79HyJZ6H9dEqxFfmGA1YnncE0xujQ64TCebhkYJKzmTJCImSVkOu9C4hZgsw6eE76n"
           "+Cg3VwEeDUFy+GXlEJWlHaEyc3HWioxgOALbUp3rOezNh+d8BDwwqvENGoePEBsz5l"
           "a6WP5lTi/HJIjAl6Hu+zHgdj1XVExeH+S52EwpZf/ylTJub0Bl5gHwf/siVE48mLMI"
           "sqrukXTZ6Zg+8EHAIvIQwJ1dKcXe8P5IoLT7VKrbkgAnolS0I8J+uH7KtErZJb5oZh"
           "S4OEwsNpaXMAr+6/wWSpircV2/e7sFLlhlKBC4Iq1MpqlZ7G3p foo@bar")

# login/password authentication
gl = gitlab.Gitlab('http://localhost:8080', email=LOGIN, password=PASSWORD)
gl.auth()
token_from_auth = gl.private_token

# token authentication from config file
gl = gitlab.Gitlab.from_config(config_files=['/tmp/python-gitlab.cfg'])
assert(token_from_auth == gl.private_token)
gl.auth()
assert(isinstance(gl.user, gitlab.objects.CurrentUser))

# user manipulations
new_user = gl.users.create({'email': 'foo@bar.com', 'username': 'foo',
                            'name': 'foo', 'password': 'foo_password'})
users_list = gl.users.list()
for user in users_list:
    if user.username == 'foo':
        break
assert(new_user.username == user.username)
assert(new_user.email == user.email)

# SSH keys
key = new_user.keys.create({'title': 'testkey', 'key': SSH_KEY})
assert(len(new_user.keys.list()) == 1)
key.delete()

new_user.delete()
assert(len(gl.users.list()) == 1)

# current user key
key = gl.user.keys.create({'title': 'testkey', 'key': SSH_KEY})
assert(len(gl.user.keys.list()) == 1)
key.delete()

# groups
user1 = gl.users.create({'email': 'user1@test.com', 'username': 'user1',
                         'name': 'user1', 'password': 'user1_pass'})
user2 = gl.users.create({'email': 'user2@test.com', 'username': 'user2',
                         'name': 'user2', 'password': 'user2_pass'})
group1 = gl.groups.create({'name': 'group1', 'path': 'group1'})
group2 = gl.groups.create({'name': 'group2', 'path': 'group2'})

assert(len(gl.groups.list()) == 2)
assert(len(gl.groups.search("1")) == 1)

group1.members.create({'access_level': gitlab.Group.OWNER_ACCESS,
                       'user_id': user1.id})
group1.members.create({'access_level': gitlab.Group.GUEST_ACCESS,
                       'user_id': user2.id})

group2.members.create({'access_level': gitlab.Group.OWNER_ACCESS,
                       'user_id': user2.id})

# Administrator belongs to the groups
assert(len(group1.members.list()) == 3)
assert(len(group2.members.list()) == 2)

group1.members.delete(user1.id)
assert(len(group1.members.list()) == 2)
member = group1.members.get(user2.id)
member.access_level = gitlab.Group.OWNER_ACCESS
member.save()
member = group1.members.get(user2.id)
assert(member.access_level == gitlab.Group.OWNER_ACCESS)

group2.members.delete(gl.user.id)

# hooks
hook = gl.hooks.create({'url': 'http://whatever.com'})
assert(len(gl.hooks.list()) == 1)
hook.delete()
assert(len(gl.hooks.list()) == 0)

# projects
admin_project = gl.projects.create({'name': 'admin_project'})
gr1_project = gl.projects.create({'name': 'gr1_project',
                                  'namespace_id': group1.id})
gr2_project = gl.projects.create({'name': 'gr2_project',
                                  'namespace_id': group2.id})

assert(len(gl.projects.all()) == 3)
assert(len(gl.projects.owned()) == 2)
assert(len(gl.projects.search("admin")) == 1)

# project content (files)
admin_project.files.create({'file_path': 'README',
                            'branch_name': 'master',
                            'content': 'Initial content',
                            'commit_message': 'Initial commit'})
readme = admin_project.files.get(file_path='README', ref='master')
readme.content = base64.b64encode("Improved README")
readme.save(branch_name="master", commit_message="new commit")
readme.delete(commit_message="Removing README")

readme = admin_project.files.create({'file_path': 'README.rst',
                                     'branch_name': 'master',
                                     'content': 'Initial content',
                                     'commit_message': 'New commit'})
assert(readme.decode() == 'Initial content')

# labels
label1 = admin_project.labels.create({'name': 'label1', 'color': '#778899'})
assert(len(admin_project.labels.list()) == 1)
label1.new_name = 'label1updated'
label1.save()
assert(label1.name == 'label1updated')
# FIXME(gpocentek): broken
# label1.delete()

# milestones
m1 = admin_project.milestones.create({'title': 'milestone1'})
assert(len(admin_project.milestones.list()) == 1)
m1.due_date = '2020-01-01T00:00:00Z'
m1.save()
m1.state_event = 'close'
m1.save()
m1 = admin_project.milestones.get(1)
assert(m1.state == 'closed')

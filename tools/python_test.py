import base64
import time

import gitlab

LOGIN = 'root'
PASSWORD = '5iveL!fe'

SSH_KEY = ("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZAjAX8vTiHD7Yi3/EzuVaDChtih"
           "79HyJZ6H9dEqxFfmGA1YnncE0xujQ64TCebhkYJKzmTJCImSVkOu9C4hZgsw6eE76n"
           "+Cg3VwEeDUFy+GXlEJWlHaEyc3HWioxgOALbUp3rOezNh+d8BDwwqvENGoePEBsz5l"
           "a6WP5lTi/HJIjAl6Hu+zHgdj1XVExeH+S52EwpZf/ylTJub0Bl5gHwf/siVE48mLMI"
           "sqrukXTZ6Zg+8EHAIvIQwJ1dKcXe8P5IoLT7VKrbkgAnolS0I8J+uH7KtErZJb5oZh"
           "S4OEwsNpaXMAr+6/wWSpircV2/e7sFLlhlKBC4Iq1MpqlZ7G3p foo@bar")
DEPLOY_KEY = ("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFdRyjJQh+1niBpXqE2I8dzjG"
              "MXFHlRjX9yk/UfOn075IdaockdU58sw2Ai1XIWFpZpfJkW7z+P47ZNSqm1gzeXI"
              "rtKa9ZUp8A7SZe8vH4XVn7kh7bwWCUirqtn8El9XdqfkzOs/+FuViriUWoJVpA6"
              "WZsDNaqINFKIA5fj/q8XQw+BcS92L09QJg9oVUuH0VVwNYbU2M2IRmSpybgC/gu"
              "uWTrnCDMmLItksATifLvRZwgdI8dr+q6tbxbZknNcgEPrI2jT0hYN9ZcjNeWuyv"
              "rke9IepE7SPBT41C+YtUX4dfDZDmczM1cE0YL/krdUCfuZHMa4ZS2YyNd6slufc"
              "vn bar@foo")

# login/password authentication
gl = gitlab.Gitlab('http://localhost:8080', email=LOGIN, password=PASSWORD)
gl.auth()
token_from_auth = gl.private_token

# token authentication from config file
gl = gitlab.Gitlab.from_config(config_files=['/tmp/python-gitlab.cfg'])
assert(token_from_auth == gl.private_token)
gl.auth()
assert(isinstance(gl.user, gitlab.v3.objects.CurrentUser))

# settings
settings = gl.settings.get()
settings.default_projects_limit = 42
settings.save()
settings = gl.settings.get()
assert(settings.default_projects_limit == 42)

# user manipulations
new_user = gl.users.create({'email': 'foo@bar.com', 'username': 'foo',
                            'name': 'foo', 'password': 'foo_password'})
users_list = gl.users.list()
for user in users_list:
    if user.username == 'foo':
        break
assert(new_user.username == user.username)
assert(new_user.email == user.email)

new_user.block()
new_user.unblock()

foobar_user = gl.users.create(
    {'email': 'foobar@example.com', 'username': 'foobar',
     'name': 'Foo Bar', 'password': 'foobar_password'})

assert gl.users.search('foobar') == [foobar_user]
usercmp = lambda x,y: cmp(x.id, y.id)
expected = sorted([new_user, foobar_user], cmp=usercmp)
actual = sorted(gl.users.search('foo'), cmp=usercmp)
assert expected == actual
assert gl.users.search('asdf') == []

assert gl.users.get_by_username('foobar') == foobar_user
assert gl.users.get_by_username('foo') == new_user
try:
    gl.users.get_by_username('asdf')
except gitlab.GitlabGetError:
    pass
else:
    assert False

# SSH keys
key = new_user.keys.create({'title': 'testkey', 'key': SSH_KEY})
assert(len(new_user.keys.list()) == 1)
key.delete()
assert(len(new_user.keys.list()) == 0)

# emails
email = new_user.emails.create({'email': 'foo2@bar.com'})
assert(len(new_user.emails.list()) == 1)
email.delete()
assert(len(new_user.emails.list()) == 0)

new_user.delete()
foobar_user.delete()
assert(len(gl.users.list()) == 3)

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

p_id = gl.groups.search('group2')[0].id
group3 = gl.groups.create({'name': 'group3', 'path': 'group3', 'parent_id': p_id})

assert(len(gl.groups.list()) == 3)
assert(len(gl.groups.search("1")) == 1)
assert(group3.parent_id == p_id)

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
sudo_project = gl.projects.create({'name': 'sudo_project'}, sudo=user1.name)

assert(len(gl.projects.all()) == 4)
assert(len(gl.projects.owned()) == 2)
assert(len(gl.projects.list(search="admin")) == 1)

# test pagination
l1 = gl.projects.list(per_page=1, page=1)
l2 = gl.projects.list(per_page=1, page=2)
assert(len(l1) == 1)
assert(len(l2) == 1)
assert(l1[0].id != l2[0].id)

# project content (files)
admin_project.files.create({'file_path': 'README',
                            'branch_name': 'master',
                            'content': 'Initial content',
                            'commit_message': 'Initial commit'})
readme = admin_project.files.get(file_path='README', ref='master')
readme.content = base64.b64encode("Improved README")
time.sleep(2)
readme.save(branch_name="master", commit_message="new commit")
readme.delete(commit_message="Removing README", branch_name="master")

admin_project.files.create({'file_path': 'README.rst',
                            'branch_name': 'master',
                            'content': 'Initial content',
                            'commit_message': 'New commit'})
readme = admin_project.files.get(file_path='README.rst', ref='master')
assert(readme.decode() == 'Initial content')

data = {
    'branch_name': 'master',
    'commit_message': 'blah blah blah',
    'actions': [
        {
            'action': 'create',
            'file_path': 'blah',
            'content': 'blah'
        }
    ]
}
admin_project.commits.create(data)

tree = admin_project.repository_tree()
assert(len(tree) == 2)
assert(tree[0]['name'] == 'README.rst')
blob = admin_project.repository_blob('master', 'README.rst')
assert(blob == 'Initial content')
archive1 = admin_project.repository_archive()
archive2 = admin_project.repository_archive('master')
assert(archive1 == archive2)

# deploy keys
deploy_key = admin_project.keys.create({'title': 'foo@bar', 'key': DEPLOY_KEY})
project_keys = admin_project.keys.list()
assert(len(project_keys) == 1)
sudo_project.keys.enable(deploy_key.id)
assert(len(sudo_project.keys.list()) == 1)
sudo_project.keys.disable(deploy_key.id)
assert(len(sudo_project.keys.list()) == 0)

# labels
label1 = admin_project.labels.create({'name': 'label1', 'color': '#778899'})
label1 = admin_project.labels.get('label1')
assert(len(admin_project.labels.list()) == 1)
label1.new_name = 'label1updated'
label1.save()
assert(label1.name == 'label1updated')
label1.subscribe()
assert(label1.subscribed == True)
label1.unsubscribe()
assert(label1.subscribed == False)
label1.delete()

# milestones
m1 = admin_project.milestones.create({'title': 'milestone1'})
assert(len(admin_project.milestones.list()) == 1)
m1.due_date = '2020-01-01T00:00:00Z'
m1.save()
m1.state_event = 'close'
m1.save()
m1 = admin_project.milestones.get(1)
assert(m1.state == 'closed')

# issues
issue1 = admin_project.issues.create({'title': 'my issue 1',
                                      'milestone_id': m1.id})
issue2 = admin_project.issues.create({'title': 'my issue 2'})
issue3 = admin_project.issues.create({'title': 'my issue 3'})
assert(len(admin_project.issues.list()) == 3)
issue3.state_event = 'close'
issue3.save()
assert(len(admin_project.issues.list(state='closed')) == 1)
assert(len(admin_project.issues.list(state='opened')) == 2)
assert(len(admin_project.issues.list(milestone='milestone1')) == 1)
assert(m1.issues()[0].title == 'my issue 1')

# tags
tag1 = admin_project.tags.create({'tag_name': 'v1.0', 'ref': 'master'})
assert(len(admin_project.tags.list()) == 1)
tag1.set_release_description('Description 1')
tag1.set_release_description('Description 2')
assert(tag1.release.description == 'Description 2')
tag1.delete()

# triggers
tr1 = admin_project.triggers.create({})
assert(len(admin_project.triggers.list()) == 1)
tr1 = admin_project.triggers.get(tr1.token)
tr1.delete()

# variables
v1 = admin_project.variables.create({'key': 'key1', 'value': 'value1'})
assert(len(admin_project.variables.list()) == 1)
v1.value = 'new_value1'
v1.save()
v1 = admin_project.variables.get(v1.key)
assert(v1.value == 'new_value1')
v1.delete()

# branches and merges
to_merge = admin_project.branches.create({'branch_name': 'branch1',
                                          'ref': 'master'})
admin_project.files.create({'file_path': 'README2.rst',
                            'branch_name': 'branch1',
                            'content': 'Initial content',
                            'commit_message': 'New commit in new branch'})
mr = admin_project.mergerequests.create({'source_branch': 'branch1',
                                         'target_branch': 'master',
                                         'title': 'MR readme2'})
ret = mr.merge()
admin_project.branches.delete('branch1')

try:
    mr.merge()
except gitlab.GitlabMRClosedError:
    pass

# stars
admin_project = admin_project.star()
assert(admin_project.star_count == 1)
admin_project = admin_project.unstar()
assert(admin_project.star_count == 0)

# project boards
#boards = admin_project.boards.list()
#assert(len(boards))
#board = boards[0]
#lists = board.lists.list()
#begin_size = len(lists)
#last_list = lists[-1]
#last_list.position = 0
#last_list.save()
#last_list.delete()
#lists = board.lists.list()
#assert(len(lists) == begin_size - 1)

# namespaces
ns = gl.namespaces.list()
assert(len(ns) != 0)
ns = gl.namespaces.list(search='root')[0]
assert(ns.kind == 'user')

# broadcast messages
msg = gl.broadcastmessages.create({'message': 'this is the message'})
msg.color = '#444444'
msg.save()
msg = gl.broadcastmessages.list()[0]
assert(msg.color == '#444444')
msg = gl.broadcastmessages.get(1)
assert(msg.color == '#444444')
msg.delete()
assert(len(gl.broadcastmessages.list()) == 0)

# notification settings
settings = gl.notificationsettings.get()
settings.level = gitlab.NOTIFICATION_LEVEL_WATCH
settings.save()
settings = gl.notificationsettings.get()
assert(settings.level == gitlab.NOTIFICATION_LEVEL_WATCH)

# services
service = admin_project.services.get(service_name='asana')
service.active = True
service.api_key = 'whatever'
service.save()
service = admin_project.services.get(service_name='asana')
assert(service.active == True)

# snippets
snippets = gl.snippets.list()
assert(len(snippets) == 0)
snippet = gl.snippets.create({'title': 'snippet1', 'file_name': 'snippet1.py',
                              'content': 'import gitlab'})
snippet = gl.snippets.get(1)
snippet.title = 'updated_title'
snippet.save()
snippet = gl.snippets.get(1)
assert(snippet.title == 'updated_title')
content = snippet.raw()
assert(content == 'import gitlab')
snippet.delete()
assert(len(gl.snippets.list()) == 0)

import base64
import os
import time

import requests

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

GPG_KEY = '''-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFn5mzYBCADH6SDVPAp1zh/hxmTi0QplkOfExBACpuY6OhzNdIg+8/528b3g
Y5YFR6T/HLv/PmeHskUj21end1C0PNG2T9dTx+2Vlh9ISsSG1kyF9T5fvMR3bE0x
Dl6S489CXZrjPTS9SHk1kF+7dwjUxLJyxF9hPiSihFefDFu3NeOtG/u8vbC1mewQ
ZyAYue+mqtqcCIFFoBz7wHKMWjIVSJSyTkXExu4OzpVvy3l2EikbvavI3qNz84b+
Mgkv/kiBlNoCy3CVuPk99RYKZ3lX1vVtqQ0OgNGQvb4DjcpyjmbKyibuZwhDjIOh
au6d1OyEbayTntd+dQ4j9EMSnEvm/0MJ4eXPABEBAAG0G0dpdGxhYlRlc3QxIDxm
YWtlQGZha2UudGxkPokBNwQTAQgAIQUCWfmbNgIbAwULCQgHAgYVCAkKCwIEFgID
AQIeAQIXgAAKCRBgxELHf8f3hF3yB/wNJlWPKY65UsB4Lo0hs1OxdxCDqXogSi0u
6crDEIiyOte62pNZKzWy8TJcGZvznRTZ7t8hXgKFLz3PRMcl+vAiRC6quIDUj+2V
eYfwaItd1lUfzvdCaC7Venf4TQ74f5vvNg/zoGwE6eRoSbjlLv9nqsxeA0rUBUQL
LYikWhVMP3TrlfgfduYvh6mfgh57BDLJ9kJVpyfxxx9YLKZbaas9sPa6LgBtR555
JziUxHmbEv8XCsUU8uoFeP1pImbNBplqE3wzJwzOMSmmch7iZzrAwfN7N2j3Wj0H
B5kQddJ9dmB4BbU0IXGhWczvdpxboI2wdY8a1JypxOdePoph/43iuQENBFn5mzYB
CADnTPY0Zf3d9zLjBNgIb3yDl94uOcKCq0twNmyjMhHzGqw+UMe9BScy34GL94Al
xFRQoaL+7P8hGsnsNku29A/VDZivcI+uxTx4WQ7OLcn7V0bnHV4d76iky2ufbUt/
GofthjDs1SonePO2N09sS4V4uK0d5N4BfCzzXgvg8etCLxNmC9BGt7AaKUUzKBO4
2QvNNaC2C/8XEnOgNWYvR36ylAXAmo0sGFXUsBCTiq1fugS9pwtaS2JmaVpZZ3YT
pMZlS0+SjC5BZYFqSmKCsA58oBRzCxQz57nR4h5VEflgD+Hy0HdW0UHETwz83E6/
U0LL6YyvhwFr6KPq5GxinSvfABEBAAGJAR8EGAEIAAkFAln5mzYCGwwACgkQYMRC
x3/H94SJgwgAlKQb10/xcL/epdDkR7vbiei7huGLBpRDb/L5fM8B5W77Qi8Xmuqj
cCu1j99ZCA5hs/vwVn8j8iLSBGMC5gxcuaar/wtmiaEvT9fO/h6q4opG7NcuiJ8H
wRj8ccJmRssNqDD913PLz7T40Ts62blhrEAlJozGVG/q7T3RAZcskOUHKeHfc2RI
YzGsC/I9d7k6uxAv1L9Nm5F2HaAQDzhkdd16nKkGaPGR35cT1JLInkfl5cdm7ldN
nxs4TLO3kZjUTgWKdhpgRNF5hwaz51ZjpebaRf/ZqRuNyX4lIRolDxzOn/+O1o8L
qG2ZdhHHmSK2LaQLFiSprUkikStNU9BqSQ==
=5OGa
-----END PGP PUBLIC KEY BLOCK-----'''
AVATAR_PATH = os.path.join(os.path.dirname(__file__), 'avatar.png')


# token authentication from config file
gl = gitlab.Gitlab.from_config(config_files=['/tmp/python-gitlab.cfg'])
gl.auth()
assert(isinstance(gl.user, gitlab.v4.objects.CurrentUser))

# markdown (need to wait for gitlab 11 to enable the test)
# html = gl.markdown('foo')
# assert('foo' in html)

success, errors = gl.lint('Invalid')
assert(success is False)
assert(errors)

# sidekiq
out = gl.sidekiq.queue_metrics()
assert(isinstance(out, dict))
assert('pages' in out['queues'])
out = gl.sidekiq.process_metrics()
assert(isinstance(out, dict))
assert('hostname' in out['processes'][0])
out = gl.sidekiq.job_stats()
assert(isinstance(out, dict))
assert('processed' in out['jobs'])
out = gl.sidekiq.compound_metrics()
assert(isinstance(out, dict))
assert('jobs' in out)
assert('processes' in out)
assert('queues' in out)

# settings
settings = gl.settings.get()
settings.default_projects_limit = 42
settings.save()
settings = gl.settings.get()
assert(settings.default_projects_limit == 42)

# users
new_user = gl.users.create({'email': 'foo@bar.com', 'username': 'foo',
                            'name': 'foo', 'password': 'foo_password',
                            'avatar': open(AVATAR_PATH, 'rb')})
avatar_url = new_user.avatar_url.replace('gitlab.test', 'localhost:8080')
uploaded_avatar = requests.get(avatar_url).content
assert(uploaded_avatar == open(AVATAR_PATH, 'rb').read())
users_list = gl.users.list()
for user in users_list:
    if user.username == 'foo':
        break
assert(new_user.username == user.username)
assert(new_user.email == user.email)

new_user.block()
new_user.unblock()

# user projects list
assert(len(new_user.projects.list()) == 0)

# events list
new_user.events.list()

foobar_user = gl.users.create(
    {'email': 'foobar@example.com', 'username': 'foobar',
     'name': 'Foo Bar', 'password': 'foobar_password'})

assert gl.users.list(search='foobar')[0].id == foobar_user.id
expected = [new_user, foobar_user]
actual = list(gl.users.list(search='foo'))
assert len(expected) == len(actual)
assert len(gl.users.list(search='asdf')) == 0
foobar_user.bio = 'This is the user bio'
foobar_user.save()

# GPG keys
gkey = new_user.gpgkeys.create({'key': GPG_KEY})
assert(len(new_user.gpgkeys.list()) == 1)
# Seems broken on the gitlab side
# gkey = new_user.gpgkeys.get(gkey.id)
gkey.delete()
assert(len(new_user.gpgkeys.list()) == 0)

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

# custom attributes
attrs = new_user.customattributes.list()
assert(len(attrs) == 0)
attr = new_user.customattributes.set('key', 'value1')
assert(len(gl.users.list(custom_attributes={'key': 'value1'})) == 1)
assert(attr.key == 'key')
assert(attr.value == 'value1')
assert(len(new_user.customattributes.list()) == 1)
attr = new_user.customattributes.set('key', 'value2')
attr = new_user.customattributes.get('key')
assert(attr.value == 'value2')
assert(len(new_user.customattributes.list()) == 1)
attr.delete()
assert(len(new_user.customattributes.list()) == 0)

# impersonation tokens
user_token = new_user.impersonationtokens.create(
    {'name': 'token1', 'scopes': ['api', 'read_user']})
l = new_user.impersonationtokens.list(state='active')
assert(len(l) == 1)
user_token.delete()
l = new_user.impersonationtokens.list(state='active')
assert(len(l) == 0)
l = new_user.impersonationtokens.list(state='inactive')
assert(len(l) == 1)

new_user.delete()
foobar_user.delete()
assert(len(gl.users.list()) == 3)

# current user mail
mail = gl.user.emails.create({'email': 'current@user.com'})
assert(len(gl.user.emails.list()) == 1)
mail.delete()
assert(len(gl.user.emails.list()) == 0)

# current user GPG keys
gkey = gl.user.gpgkeys.create({'key': GPG_KEY})
assert(len(gl.user.gpgkeys.list()) == 1)
# Seems broken on the gitlab side
gkey = gl.user.gpgkeys.get(gkey.id)
gkey.delete()
assert(len(gl.user.gpgkeys.list()) == 0)

# current user key
key = gl.user.keys.create({'title': 'testkey', 'key': SSH_KEY})
assert(len(gl.user.keys.list()) == 1)
key.delete()
assert(len(gl.user.keys.list()) == 0)

# templates
assert(gl.dockerfiles.list())
dockerfile = gl.dockerfiles.get('Node')
assert(dockerfile.content is not None)

assert(gl.gitignores.list())
gitignore = gl.gitignores.get('Node')
assert(gitignore.content is not None)

assert(gl.gitlabciymls.list())
gitlabciyml = gl.gitlabciymls.get('Nodejs')
assert(gitlabciyml.content is not None)

assert(gl.licenses.list())
license = gl.licenses.get('bsd-2-clause', project='mytestproject',
                          fullname='mytestfullname')
assert('mytestfullname' in license.content)

# groups
user1 = gl.users.create({'email': 'user1@test.com', 'username': 'user1',
                         'name': 'user1', 'password': 'user1_pass'})
user2 = gl.users.create({'email': 'user2@test.com', 'username': 'user2',
                         'name': 'user2', 'password': 'user2_pass'})
group1 = gl.groups.create({'name': 'group1', 'path': 'group1'})
group2 = gl.groups.create({'name': 'group2', 'path': 'group2'})

p_id = gl.groups.list(search='group2')[0].id
group3 = gl.groups.create({'name': 'group3', 'path': 'group3', 'parent_id': p_id})

assert(len(gl.groups.list()) == 3)
assert(len(gl.groups.list(search='oup1')) == 1)
assert(group3.parent_id == p_id)
assert(group2.subgroups.list()[0].id == group3.id)

group1.members.create({'access_level': gitlab.const.OWNER_ACCESS,
                       'user_id': user1.id})
group1.members.create({'access_level': gitlab.const.GUEST_ACCESS,
                       'user_id': user2.id})

group2.members.create({'access_level': gitlab.const.OWNER_ACCESS,
                       'user_id': user2.id})

# Administrator belongs to the groups
assert(len(group1.members.list()) == 3)
assert(len(group2.members.list()) == 2)

group1.members.delete(user1.id)
assert(len(group1.members.list()) == 2)
assert(len(group1.members.all()))
member = group1.members.get(user2.id)
member.access_level = gitlab.const.OWNER_ACCESS
member.save()
member = group1.members.get(user2.id)
assert(member.access_level == gitlab.const.OWNER_ACCESS)

group2.members.delete(gl.user.id)

# group custom attributes
attrs = group2.customattributes.list()
assert(len(attrs) == 0)
attr = group2.customattributes.set('key', 'value1')
assert(len(gl.groups.list(custom_attributes={'key': 'value1'})) == 1)
assert(attr.key == 'key')
assert(attr.value == 'value1')
assert(len(group2.customattributes.list()) == 1)
attr = group2.customattributes.set('key', 'value2')
attr = group2.customattributes.get('key')
assert(attr.value == 'value2')
assert(len(group2.customattributes.list()) == 1)
attr.delete()
assert(len(group2.customattributes.list()) == 0)

# group notification settings
settings = group2.notificationsettings.get()
settings.level = 'disabled'
settings.save()
settings = group2.notificationsettings.get()
assert(settings.level == 'disabled')

# group badges
badge_image = 'http://example.com'
badge_link = 'http://example/img.svg'
badge = group2.badges.create({'link_url': badge_link, 'image_url': badge_image})
assert(len(group2.badges.list()) == 1)
badge.image_url = 'http://another.example.com'
badge.save()
badge = group2.badges.get(badge.id)
assert(badge.image_url == 'http://another.example.com')
badge.delete()
assert(len(group2.badges.list()) == 0)

# group milestones
gm1 = group1.milestones.create({'title': 'groupmilestone1'})
assert(len(group1.milestones.list()) == 1)
gm1.due_date = '2020-01-01T00:00:00Z'
gm1.save()
gm1.state_event = 'close'
gm1.save()
gm1 = group1.milestones.get(gm1.id)
assert(gm1.state == 'closed')
assert(len(gm1.issues()) == 0)
assert(len(gm1.merge_requests()) == 0)

# group variables
group1.variables.create({'key': 'foo', 'value': 'bar'})
g_v = group1.variables.get('foo')
assert(g_v.value == 'bar')
g_v.value = 'baz'
g_v.save()
g_v = group1.variables.get('foo')
assert(g_v.value == 'baz')
assert(len(group1.variables.list()) == 1)
g_v.delete()
assert(len(group1.variables.list()) == 0)

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

assert(len(gl.projects.list(owned=True)) == 2)
assert(len(gl.projects.list(search="admin")) == 1)

# test pagination
l1 = gl.projects.list(per_page=1, page=1)
l2 = gl.projects.list(per_page=1, page=2)
assert(len(l1) == 1)
assert(len(l2) == 1)
assert(l1[0].id != l2[0].id)

# group custom attributes
attrs = admin_project.customattributes.list()
assert(len(attrs) == 0)
attr = admin_project.customattributes.set('key', 'value1')
assert(len(gl.projects.list(custom_attributes={'key': 'value1'})) == 1)
assert(attr.key == 'key')
assert(attr.value == 'value1')
assert(len(admin_project.customattributes.list()) == 1)
attr = admin_project.customattributes.set('key', 'value2')
attr = admin_project.customattributes.get('key')
assert(attr.value == 'value2')
assert(len(admin_project.customattributes.list()) == 1)
attr.delete()
assert(len(admin_project.customattributes.list()) == 0)

# project pages domains
domain = admin_project.pagesdomains.create({'domain': 'foo.domain.com'})
assert(len(admin_project.pagesdomains.list()) == 1)
assert(len(gl.pagesdomains.list()) == 1)
domain = admin_project.pagesdomains.get('foo.domain.com')
assert(domain.domain == 'foo.domain.com')
domain.delete()
assert(len(admin_project.pagesdomains.list()) == 0)

# project content (files)
admin_project.files.create({'file_path': 'README',
                            'branch': 'master',
                            'content': 'Initial content',
                            'commit_message': 'Initial commit'})
readme = admin_project.files.get(file_path='README', ref='master')
readme.content = base64.b64encode(b"Improved README").decode()
time.sleep(2)
readme.save(branch="master", commit_message="new commit")
readme.delete(commit_message="Removing README", branch="master")

admin_project.files.create({'file_path': 'README.rst',
                            'branch': 'master',
                            'content': 'Initial content',
                            'commit_message': 'New commit'})
readme = admin_project.files.get(file_path='README.rst', ref='master')
# The first decode() is the ProjectFile method, the second one is the bytes
# object method
assert(readme.decode().decode() == 'Initial content')

data = {
    'branch': 'master',
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
assert('@@' in admin_project.commits.list()[0].diff()[0]['diff'])

# commit status
commit = admin_project.commits.list()[0]
status = commit.statuses.create({'state': 'success', 'sha': commit.id})
assert(len(commit.statuses.list()) == 1)

assert(commit.refs())
assert(commit.merge_requests() is not None)

# commit comment
commit.comments.create({'note': 'This is a commit comment'})
assert(len(commit.comments.list()) == 1)

# commit discussion
count = len(commit.discussions.list())
discussion = commit.discussions.create({'body': 'Discussion body'})
assert(len(commit.discussions.list()) == (count + 1))
d_note = discussion.notes.create({'body': 'first note'})
d_note_from_get = discussion.notes.get(d_note.id)
d_note_from_get.body = 'updated body'
d_note_from_get.save()
discussion = commit.discussions.get(discussion.id)
assert(discussion.attributes['notes'][-1]['body'] == 'updated body')
d_note_from_get.delete()
discussion = commit.discussions.get(discussion.id)
assert(len(discussion.attributes['notes']) == 1)

# housekeeping
admin_project.housekeeping()

# repository
tree = admin_project.repository_tree()
assert(len(tree) != 0)
assert(tree[0]['name'] == 'README.rst')
blob_id = tree[0]['id']
blob = admin_project.repository_raw_blob(blob_id)
assert(blob.decode() == 'Initial content')
archive1 = admin_project.repository_archive()
archive2 = admin_project.repository_archive('master')
assert(archive1 == archive2)
snapshot = admin_project.snapshot()

# project file uploads
filename = "test.txt"
file_contents = "testing contents"
uploaded_file = admin_project.upload(filename, file_contents)
assert(uploaded_file["alt"] == filename)
assert(uploaded_file["url"].startswith("/uploads/"))
assert(uploaded_file["url"].endswith("/" + filename))
assert(uploaded_file["markdown"] == "[{}]({})".format(
    uploaded_file["alt"],
    uploaded_file["url"],
))

# environments
admin_project.environments.create({'name': 'env1', 'external_url':
                                   'http://fake.env/whatever'})
envs = admin_project.environments.list()
assert(len(envs) == 1)
env = envs[0]
env.external_url = 'http://new.env/whatever'
env.save()
env = admin_project.environments.list()[0]
assert(env.external_url == 'http://new.env/whatever')
env.stop()
env.delete()
assert(len(admin_project.environments.list()) == 0)

# project events
admin_project.events.list()

# forks
fork = admin_project.forks.create({'namespace': user1.username})
p = gl.projects.get(fork.id)
assert(p.forked_from_project['id'] == admin_project.id)

forks = admin_project.forks.list()
assert(fork.id in map(lambda p: p.id, forks))

# project hooks
hook = admin_project.hooks.create({'url': 'http://hook.url'})
assert(len(admin_project.hooks.list()) == 1)
hook.note_events = True
hook.save()
hook = admin_project.hooks.get(hook.id)
assert(hook.note_events is True)
hook.delete()

# deploy keys
deploy_key = admin_project.keys.create({'title': 'foo@bar', 'key': DEPLOY_KEY})
project_keys = list(admin_project.keys.list())
assert(len(project_keys) == 1)

sudo_project.keys.enable(deploy_key.id)
assert(len(sudo_project.keys.list()) == 1)
sudo_project.keys.delete(deploy_key.id)
assert(len(sudo_project.keys.list()) == 0)

# labels
label1 = admin_project.labels.create({'name': 'label1', 'color': '#778899'})
label1 = admin_project.labels.list()[0]
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
m1 = admin_project.milestones.get(m1.id)
assert(m1.state == 'closed')
assert(len(m1.issues()) == 0)
assert(len(m1.merge_requests()) == 0)

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
assert(m1.issues().next().title == 'my issue 1')
note = issue1.notes.create({'body': 'This is an issue note'})
assert(len(issue1.notes.list()) == 1)
emoji = note.awardemojis.create({'name': 'tractor'})
assert(len(note.awardemojis.list()) == 1)
emoji.delete()
assert(len(note.awardemojis.list()) == 0)
note.delete()
assert(len(issue1.notes.list()) == 0)
assert(isinstance(issue1.user_agent_detail(), dict))

assert(issue1.user_agent_detail()['user_agent'])
assert(issue1.participants())

discussion = issue1.discussions.create({'body': 'Discussion body'})
assert(len(issue1.discussions.list()) == 1)
d_note = discussion.notes.create({'body': 'first note'})
d_note_from_get = discussion.notes.get(d_note.id)
d_note_from_get.body = 'updated body'
d_note_from_get.save()
discussion = issue1.discussions.get(discussion.id)
assert(discussion.attributes['notes'][-1]['body'] == 'updated body')
d_note_from_get.delete()
discussion = issue1.discussions.get(discussion.id)
assert(len(discussion.attributes['notes']) == 1)

# tags
tag1 = admin_project.tags.create({'tag_name': 'v1.0', 'ref': 'master'})
assert(len(admin_project.tags.list()) == 1)
tag1.set_release_description('Description 1')
tag1.set_release_description('Description 2')
assert(tag1.release['description'] == 'Description 2')
tag1.delete()

# project snippet
admin_project.snippets_enabled = True
admin_project.save()
snippet = admin_project.snippets.create(
    {'title': 'snip1', 'file_name': 'foo.py', 'code': 'initial content',
     'visibility': gitlab.v4.objects.VISIBILITY_PRIVATE}
)

assert(snippet.user_agent_detail()['user_agent'])

discussion = snippet.discussions.create({'body': 'Discussion body'})
assert(len(snippet.discussions.list()) == 1)
d_note = discussion.notes.create({'body': 'first note'})
d_note_from_get = discussion.notes.get(d_note.id)
d_note_from_get.body = 'updated body'
d_note_from_get.save()
discussion = snippet.discussions.get(discussion.id)
assert(discussion.attributes['notes'][-1]['body'] == 'updated body')
d_note_from_get.delete()
discussion = snippet.discussions.get(discussion.id)
assert(len(discussion.attributes['notes']) == 1)

snippet.file_name = 'bar.py'
snippet.save()
snippet = admin_project.snippets.get(snippet.id)
assert(snippet.content().decode() == 'initial content')
assert(snippet.file_name == 'bar.py')
size = len(admin_project.snippets.list())
snippet.delete()
assert(len(admin_project.snippets.list()) == (size - 1))

# triggers
tr1 = admin_project.triggers.create({'description': 'trigger1'})
assert(len(admin_project.triggers.list()) == 1)
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
to_merge = admin_project.branches.create({'branch': 'branch1',
                                          'ref': 'master'})
admin_project.files.create({'file_path': 'README2.rst',
                            'branch': 'branch1',
                            'content': 'Initial content',
                            'commit_message': 'New commit in new branch'})
mr = admin_project.mergerequests.create({'source_branch': 'branch1',
                                         'target_branch': 'master',
                                         'title': 'MR readme2'})

# discussion
discussion = mr.discussions.create({'body': 'Discussion body'})
assert(len(mr.discussions.list()) == 1)
d_note = discussion.notes.create({'body': 'first note'})
d_note_from_get = discussion.notes.get(d_note.id)
d_note_from_get.body = 'updated body'
d_note_from_get.save()
discussion = mr.discussions.get(discussion.id)
assert(discussion.attributes['notes'][-1]['body'] == 'updated body')
d_note_from_get.delete()
discussion = mr.discussions.get(discussion.id)
assert(len(discussion.attributes['notes']) == 1)

# basic testing: only make sure that the methods exist
mr.commits()
mr.changes()
assert(mr.participants())

mr.merge()
admin_project.branches.delete('branch1')

try:
    mr.merge()
except gitlab.GitlabMRClosedError:
    pass

# protected branches
p_b = admin_project.protectedbranches.create({'name': '*-stable'})
assert(p_b.name == '*-stable')
p_b = admin_project.protectedbranches.get('*-stable')
# master is protected by default when a branch has been created
assert(len(admin_project.protectedbranches.list()) == 2)
admin_project.protectedbranches.delete('master')
p_b.delete()
assert(len(admin_project.protectedbranches.list()) == 0)

# stars
admin_project.star()
assert(admin_project.star_count == 1)
admin_project.unstar()
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

# project badges
badge_image = 'http://example.com'
badge_link = 'http://example/img.svg'
badge = admin_project.badges.create({'link_url': badge_link, 'image_url': badge_image})
assert(len(admin_project.badges.list()) == 1)
badge.image_url = 'http://another.example.com'
badge.save()
badge = admin_project.badges.get(badge.id)
assert(badge.image_url == 'http://another.example.com')
badge.delete()
assert(len(admin_project.badges.list()) == 0)

# project wiki
wiki_content = 'Wiki page content'
wp = admin_project.wikis.create({'title': 'wikipage', 'content': wiki_content})
assert(len(admin_project.wikis.list()) == 1)
wp = admin_project.wikis.get(wp.slug)
assert(wp.content == wiki_content)
# update and delete seem broken
# wp.content = 'new content'
# wp.save()
# wp.delete()
# assert(len(admin_project.wikis.list()) == 0)

# namespaces
ns = gl.namespaces.list(all=True)
assert(len(ns) != 0)
ns = gl.namespaces.list(search='root', all=True)[0]
assert(ns.kind == 'user')

# features
feat = gl.features.set('foo', 30)
assert(feat.name == 'foo')
assert(len(gl.features.list()) == 1)
feat.delete()
assert(len(gl.features.list()) == 0)

# broadcast messages
msg = gl.broadcastmessages.create({'message': 'this is the message'})
msg.color = '#444444'
msg.save()
msg = gl.broadcastmessages.list(all=True)[0]
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
service = admin_project.services.get('asana')
service.api_key = 'whatever'
service.save()
service = admin_project.services.get('asana')
assert(service.active == True)
service.delete()
service = admin_project.services.get('asana')
assert(service.active == False)

# snippets
snippets = gl.snippets.list(all=True)
assert(len(snippets) == 0)
snippet = gl.snippets.create({'title': 'snippet1', 'file_name': 'snippet1.py',
                              'content': 'import gitlab'})
snippet = gl.snippets.get(snippet.id)
snippet.title = 'updated_title'
snippet.save()
snippet = gl.snippets.get(snippet.id)
assert(snippet.title == 'updated_title')
content = snippet.content()
assert(content.decode() == 'import gitlab')

assert(snippet.user_agent_detail()['user_agent'])

snippet.delete()
snippets = gl.snippets.list(all=True)
assert(len(snippets) == 0)

# user activities
gl.user_activities.list()

# events
gl.events.list()

# rate limit
settings = gl.settings.get()
settings.throttle_authenticated_api_enabled = True
settings.throttle_authenticated_api_requests_per_period = 1
settings.throttle_authenticated_api_period_in_seconds = 3
settings.save()
projects = list()
for i in range(0, 20):
    projects.append(gl.projects.create(
        {'name': str(i) + "ok"}))

error_message = None
for i in range(20, 40):
    try:
        projects.append(
            gl.projects.create(
                {'name': str(i) + 'shouldfail'}, obey_rate_limit=False))
    except gitlab.GitlabCreateError as e:
        error_message = e.error_message
        break
assert 'Retry later' in error_message.decode()
[current_project.delete() for current_project in projects]
settings.throttle_authenticated_api_enabled = False
settings.save()

# project import/export
ex = admin_project.exports.create({})
ex.refresh()
count = 0
while ex.export_status != 'finished':
    time.sleep(1)
    ex.refresh()
    count += 1
    if count == 10:
        raise Exception('Project export taking too much time')
with open('/tmp/gitlab-export.tgz', 'wb') as f:
    ex.download(streamed=True, action=f.write)

output = gl.projects.import_project(open('/tmp/gitlab-export.tgz', 'rb'),
                               'imported_project')
project_import = gl.projects.get(output['id'], lazy=True).imports.get()
count = 0
while project_import.import_status != 'finished':
    time.sleep(1)
    project_import.refresh()
    count += 1
    if count == 10:
        raise Exception('Project import taking too much time')

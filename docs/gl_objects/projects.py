# list
# Active projects
projects = gl.projects.list()
# Archived projects
projects = gl.projects.list(archived=1)
# Limit to projects with a defined visibility
projects = gl.projects.list(visibility='public')

# List owned projects
projects = gl.projects.owned()

# List starred projects
projects = gl.projects.starred()

# List all the projects
projects = gl.projects.all()

# Search projects
projects = gl.projects.list(search='keyword')
# end list

# get
# Get a project by ID
project = gl.projects.get(10)
# Get a project by userspace/name
project = gl.projects.get('myteam/myproject')
# end get

# create
project = gl.projects.create({'name': 'project1'})
# end create

# user create
alice = gl.users.list(username='alice')[0]
user_project = alice.projects.create({'name': 'project'})
user_projects = alice.projects.list()
# end user create

# update
project.snippets_enabled = 1
project.save()
# end update

# delete
gl.projects.delete(1)
# or
project.delete()
# end delete

# fork
fork = project.forks.create({})

# fork to a specific namespace
fork = project.forks.create({'namespace': 'myteam'})
# end fork

# forkrelation
project.create_fork_relation(source_project.id)
project.delete_fork_relation()
# end forkrelation

# star
project.star()
project.unstar()
# end star

# archive
project.archive()
project.unarchive()
# end archive

# events list
gl.project_events.list(project_id=1)
# or
project.events.list()
# end events list

# members list
members = project.members.list()
# end members list

# members search
members = project.members.list(query='bar')
# end members search

# members get
member = project.members.get(1)
# end members get

# members add
member = project.members.create({'user_id': user.id, 'access_level':
                                 gitlab.DEVELOPER_ACCESS})
# end members add

# members update
member.access_level = gitlab.MASTER_ACCESS
member.save()
# end members update

# members delete
project.members.delete(user.id)
# or
member.delete()
# end members delete

# share
project.share(group.id, gitlab.DEVELOPER_ACCESS)
# end share

# hook list
hooks = project.hooks.list()
# end hook list

# hook get
hook = project.hooks.get(1)
# end hook get

# hook create
hook = gl.project_hooks.create({'url': 'http://my/action/url',
                                'push_events': 1},
                               project_id=1)
# or
hook = project.hooks.create({'url': 'http://my/action/url', 'push_events': 1})
# end hook create

# hook update
hook.push_events = 0
hook.save()
# end hook update

# hook delete
project.hooks.delete(1)
# or
hook.delete()
# end hook delete

# repository tree
# list the content of the root directory for the default branch
items = project.repository_tree()

# list the content of a subdirectory on a specific branch
items = project.repository_tree(path='docs', ref='branch1')
# end repository tree

# repository blob
items = project.repository_tree(path='docs', ref='branch1')
file_info = p.repository_blob(items[0]['id'])
content = base64.b64decode(file_info['content'])
size = file_info['size']
# end repository blob

# repository raw_blob
# find the id for the blob (simple search)
id = [d['id'] for d in p.repository_tree() if d['name'] == 'README.rst'][0]

# get the content
file_content = p.repository_raw_blob(id)
# end repository raw_blob

# repository compare
result = project.repository_compare('master', 'branch1')

# get the commits
for commit in result['commits']:
    print(commit)

# get the diffs
for file_diff in result['diffs']:
    print(file_diff)
# end repository compare

# repository archive
# get the archive for the default branch
tgz = project.repository_archive()

# get the archive for a branch/tag/commit
tgz = project.repository_archive(sha='4567abc')
# end repository archive

# repository contributors
contributors = project.repository_contributors()
# end repository contributors

# housekeeping
project.housekeeping()
# end housekeeping

# files get
f = project.files.get(file_path='README.rst', ref='master')

# get the base64 encoded content
print(f.content)

# get the decoded content
print(f.decode())
# end files get

# files create
# v4
f = project.files.create({'file_path': 'testfile',
                          'branch': 'master',
                          'content': file_content,
                          'commit_message': 'Create testfile'})

# v3
f = project.files.create({'file_path': 'testfile',
                          'branch_name': 'master',
                          'content': file_content,
                          'commit_message': 'Create testfile'})
# end files create

# files update
f.content = 'new content'
f.save(branch='master', commit_message='Update testfile')  # v4
f.save(branch_name='master', commit_message='Update testfile')  # v3

# or for binary data
# Note: decode() is required with python 3 for data serialization. You can omit
# it with python 2
f.content = base64.b64encode(open('image.png').read()).decode()
f.save(branch='master', commit_message='Update testfile', encoding='base64')
# end files update

# files delete
f.delete(commit_message='Delete testfile')
# end files delete

# tags list
tags = project.tags.list()
# end tags list

# tags get
tag = project.tags.get('1.0')
# end tags get

# tags create
tag = project.tags.create({'tag_name': '1.0', 'ref': 'master'})
# end tags create

# tags delete
project.tags.delete('1.0')
# or
tag.delete()
# end tags delete

# tags release
tag.set_release_description('awesome v1.0 release')
# end tags release

# snippets list
snippets = project.snippets.list()
# end snippets list

# snippets get
snippets = project.snippets.list(snippet_id)
# end snippets get

# snippets create
snippet = project.snippets.create({'title': 'sample 1',
                                   'file_name': 'foo.py',
                                   'code': 'import gitlab',
                                   'visibility_level':
                                   gitlab.VISIBILITY_PRIVATE})
# end snippets create

# snippets content
print(snippet.content())
# end snippets content

# snippets update
snippet.code = 'import gitlab\nimport whatever'
snippet.save
# end snippets update

# snippets delete
project.snippets.delete(snippet_id)
# or
snippet.delete()
# end snippets delete

# notes list
i_notes = issue.notes.list()
mr_notes = mr.notes.list()
s_notes = snippet.notes.list()
# end notes list

# notes get
i_note = issue.notes.get(note_id)
mr_note = mr.notes.get(note_id)
s_note = snippet.notes.get(note_id)
# end notes get

# notes create
i_note = issue.notes.create({'body': 'note content'})
mr_note = mr.notes.create({'body': 'note content'})
s_note = snippet.notes.create({'body': 'note content'})
# end notes create

# notes update
note.body = 'updated note content'
note.save()
# end notes update

# notes delete
note.delete()
# end notes delete

# service get
# For v3
service = project.services.get(service_name='asana', project_id=1)
# For v4
service = project.services.get('asana')
# display its status (enabled/disabled)
print(service.active)
# end service get

# service list
services = gl.project_services.available()
# end service list

# service update
service.api_key = 'randomkey'
service.save()
# end service update

# service delete
service.delete()
# end service delete

# pipeline list
pipelines = project.pipelines.list()
# end pipeline list

# pipeline get
pipeline = project.pipelines.get(pipeline_id)
# end pipeline get

# pipeline create
pipeline = project.pipelines.create({'ref': 'master'})
# end pipeline create

# pipeline retry
pipeline.retry()
# end pipeline retry

# pipeline cancel
pipeline.cancel()
# end pipeline cancel

# boards list
boards = project.boards.list()
# end boards list

# boards get
board = project.boards.get(board_id)
# end boards get

# board lists list
b_lists = board.lists.list()
# end board lists list

# board lists get
b_list = board.lists.get(list_id)
# end board lists get

# board lists create
# First get a ProjectLabel
label = get_or_create_label()
# Then use its ID to create the new board list
b_list = board.lists.create({'label_id': label.id})
# end board lists create

# board lists update
b_list.position = 2
b_list.save()
# end board lists update

# board lists delete
b_list.delete()
# end board lists delete

# project file upload by path
# Or provide a full path to the uploaded file
project.upload("filename.txt", filepath="/some/path/filename.txt")
# end project file upload by path

# project file upload with data
# Upload a file using its filename and filedata
project.upload("filename.txt", filedata="Raw data")
# end project file upload with data

# project file upload markdown
uploaded_file = project.upload("filename.txt", filedata="data")
issue = project.issues.get(issue_id)
issue.notes.create({
    "body": "See the attached file: {}".format(uploaded_file["markdown"])
})
# end project file upload markdown

# project file upload markdown custom
uploaded_file = project.upload("filename.txt", filedata="data")
issue = project.issues.get(issue_id)
issue.notes.create({
    "body": "See the [attached file]({})".format(uploaded_file["url"])
})
# end project file upload markdown custom

# users list
users = p.users.list()

# search for users
users = p.users.list(search='pattern')
# end users list

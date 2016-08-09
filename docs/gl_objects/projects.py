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
projects = gl.projects.search('query')
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
alice gl.users.list(username='alice')[0]
user_project = gl.user_projects.create({'name': 'project',
                                        'user_id': alice.id})
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
fork = gl.project_forks.create({}, project_id=1)
# or
fork = project.forks.create({})
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
project.archive_()
project.unarchive_()
# end archive

# events list
gl.project_events.list(project_id=1)
# or
project.events.list()
# end events list

# members list
members = gl.project_members.list()
# or
members = project.members.list()
# end members list

# members search
members = gl.project_members.list(query='foo')
# or
members = project.members.list(query='bar')
# end members search

# members get
member = gl.project_members.get(1)
# or
member = project.members.get(1)
# end members get

# members add
member = gl.project_members.create({'user_id': user.id, 'access_level':
                                    gitlab.Group.DEVELOPER_ACCESS},
                                   project_id=1)
# or
member = project.members.create({'user_id': user.id, 'access_level':
                                 gitlab.Group.DEVELOPER_ACCESS})
# end members add

# members update
member.access_level = gitlab.Group.MASTER_ACCESS
member.save()
# end members update

# members delete
gl.project_members.delete(user.id, project_id=1)
# or
project.members.delete(user.id)
# or
member.delete()
# end members delete

# share
project.share(group.id, group.DEVELOPER_ACCESS)
# end share

# hook list
hooks = gl.project_hooks.list(project_id=1)
# or
hooks = project.hooks.list()
# end hook list

# hook get
hook = gl.project_hooks.get(1, project_id=1)
# or
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
gl.project_hooks.delete(1, project_id=1)
# or
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
file_content = p.repository_blob('master', 'README.rst')
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
for i in commit:
    print(result.commits)

# get the diffs
for file_diff in commit.diffs:
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

# files get
f = gl.project_files.get(file_path='README.rst', ref='master',
                         project_id=1)
# or
f = project.files.get(file_path='README.rst', ref='master')

# get the base64 encoded content
print(f.content)

# get the decoded content
print(f.decode())
# end files get

# files create
f = gl.project_files.create({'file_path': 'testfile',
                             'branch_name': 'master',
                             'content': file_content,
                             'commit_message': 'Create testfile'},
                            project_id=1)
# or
f = project.files.create({'file_path': 'testfile',
                          'branch_name': 'master',
                          'content': file_content,
                          'commit_message': 'Create testfile'})
# end files create

# files update
f.content = 'new content'
f.save(branch='master', commit_message='Update testfile')

# or for binary data
f.content = base64.b64encode(open('image.png').read())
f.save(branch='master', commit_message='Update testfile', encoding='base64')
# end files update

# files delete
gl.project_files.delete({'file_path': 'testfile',
                         'branch_name': 'master',
                         'commit_message': 'Delete testfile'},
                        project_id=1)
# or
project.files.delete({'file_path': 'testfile',
                      'branch_name': 'master',
                      'commit_message': 'Delete testfile'})
# or
f.delete(commit_message='Delete testfile')
# end files delete

# tags list
tags = gl.project_tags.list(project_id=1)
# or
tags = project.tags.list()
# end tags list

# tags get
tag = gl.project_tags.list('1.0', project_id=1)
# or
tags = project.tags.list('1.0')
# end tags get

# tags create
tag = gl.project_tags.create({'tag_name': '1.0', 'ref': 'master'},
                             project_id=1)
# or
tag = project.tags.create({'tag_name': '1.0', 'ref': 'master'})
# end tags create

# tags delete
gl.project_tags.delete('1.0', project_id=1)
# or
project.tags.delete('1.0')
# or
tag.delete()
# end tags delete

# tags release
tag.set_release_description('awesome v1.0 release')
# end tags release

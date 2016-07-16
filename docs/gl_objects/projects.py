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
fork = gl.project_forks.create(project_id=1)
# or
fork = project.fork()
# end fork

# star
p.star()
p.unstar()
# end star

# archive
p.archive_()
p.unarchive_()
# end archive

# events list
gl.project_events.list(project_id=1)
# or
project.events.list()
# end events list

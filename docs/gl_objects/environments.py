# list
environments = gl.project_environments.list(project_id=1)
# or
environments = project.environments.list()
# end list

# get
environment = gl.project_environments.get(environment_id, project_id=1)
# or
environment = project.environments.get(environment_id)
# end get

# create
environment = gl.project_environments.create({'name': 'production'},
                                             project_id=1)
# or
environment = project.environments.create({'name': 'production'})
# end create

# update
environment.external_url = 'http://foo.bar.com'
environment.save()
# end update

# delete
environment = gl.project_environments.delete(environment_id, project_id=1)
# or
environment = project.environments.list(environment_id)
# or
environment.delete()
# end delete

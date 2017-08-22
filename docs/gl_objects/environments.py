# list
environments = project.environments.list()
# end list

# get
environment = project.environments.get(environment_id)
# end get

# create
environment = project.environments.create({'name': 'production'})
# end create

# update
environment.external_url = 'http://foo.bar.com'
environment.save()
# end update

# delete
environment = project.environments.delete(environment_id)
# or
environment.delete()
# end delete

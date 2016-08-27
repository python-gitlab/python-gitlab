# list
deployments = gl.project_deployments.list(project_id=1)
# or
deployments = project.deployments.list()
# end list

# get
deployment = gl.project_deployments.get(deployment_id, project_id=1)
# or
deployment = project.deployments.get(deployment_id)
# end get

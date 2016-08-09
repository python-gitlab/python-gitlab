# list
milestones = gl.project_milestones.list(project_id=1)
# or
milestones = project.milestones.list()
# end list

# filter
milestones = gl.project_milestones.list(project_id=1, state='closed')
# or
milestones = project.milestones.list(state='closed')
# end filter

# get
milestone = gl.project_milestones.get(milestone_id, project_id=1)
# or
milestone = project.milestones.get(milestone_id)
# end get

# create
milestone = gl.project_milestones.create({'title': '1.0'}, project_id=1)
# or
milestone = project.milestones.create({'title': '1.0'})
# end create

# update
milestone.description = 'v 1.0 release'
milestone.save()
# end update

# state
# close a milestone
milestone.state_event = 'close'
milestone.save

# activate a milestone
milestone.state_event = 'activate'
m.save()
# end state

# issues
issues = milestone.issues()
# end issues

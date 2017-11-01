# list
p_milestones = project.milestones.list()
g_milestones = group.milestones.list()
# end list

# filter
p_milestones = project.milestones.list(state='closed')
g_milestones = group.milestones.list(state='active')
# end filter

# get
p_milestone = project.milestones.get(milestone_id)
g_milestone = group.milestones.get(milestone_id)
# end get

# create
milestone = project.milestones.create({'title': '1.0'})
# end create

# update
milestone.description = 'v 1.0 release'
milestone.save()
# end update

# state
# close a milestone
milestone.state_event = 'close'
milestone.save()

# activate a milestone
milestone.state_event = 'activate'
milestone.save()
# end state

# issues
issues = milestone.issues()
# end issues

# merge_requests
merge_requests = milestone.merge_requests()
# end merge_requests

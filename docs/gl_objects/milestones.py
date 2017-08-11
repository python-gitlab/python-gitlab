# list
milestones = project.milestones.list()
# end list

# filter
milestones = project.milestones.list(state='closed')
# end filter

# get
milestone = project.milestones.get(milestone_id)
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


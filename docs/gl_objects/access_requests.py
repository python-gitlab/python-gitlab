# list
p_ars = project.accessrequests.list()
g_ars = group.accessrequests.list()
# end list

# get
p_ar = project.accessrequests.get(user_id)
g_ar = group.accessrequests.get(user_id)
# end get

# create
p_ar = project.accessrequests.create({})
g_ar = group.accessrequests.create({})
# end create

# approve
ar.approve()  # defaults to DEVELOPER level
ar.approve(access_level=gitlab.MASTER_ACCESS)  # explicitly set access level
# end approve

# delete
project.accessrequests.delete(user_id)
group.accessrequests.delete(user_id)
# or
ar.delete()
# end delete

# list
p_ars = gl.project_accessrequests.list(project_id=1)
g_ars = gl.group_accessrequests.list(group_id=1)
# or
p_ars = project.accessrequests.list()
g_ars = group.accessrequests.list()
# end list

# get
p_ar = gl.project_accessrequests.get(user_id, project_id=1)
g_ar = gl.group_accessrequests.get(user_id, group_id=1)
# or
p_ar = project.accessrequests.get(user_id)
g_ar = group.accessrequests.get(user_id)
# end get

# create
p_ar = gl.project_accessrequests.create({}, project_id=1)
g_ar = gl.group_accessrequests.create({}, group_id=1)
# or
p_ar = project.accessrequests.create({})
g_ar = group.accessrequests.create({})
# end create

# approve
ar.approve()  # defaults to DEVELOPER level
ar.approve(access_level=gitlab.MASTER_ACCESS)  # explicitly set access level
# end approve

# delete
gl.project_accessrequests.delete(user_id, project_id=1)
gl.group_accessrequests.delete(user_id, group_id=1)
# or
project.accessrequests.delete(user_id)
group.accessrequests.delete(user_id)
# or
ar.delete()
# end delete

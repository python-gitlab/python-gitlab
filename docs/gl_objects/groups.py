# list
groups = gl.groups.list()
# end list

# search
groups = gl.groups.search('group')
# end search

# get
group = gl.groups.get(group_id)
# end get

# projects list
projects = group.projects.list()
# or
projects = gl.group_projects.list(group_id)
# end projects list

# create
group = gl.groups.create({'name': 'group1', 'path': 'group1'})
# end create

# update
group.description = 'My awesome group'
group.save()
# end update

# delete
gl.group.delete(group_id)
# or
group.delete()
# end delete

# member list
members = gl.group_members.list(group_id=1)
# or
members = group.members.list()
# end member list

# member get
members = gl.group_members.get(member_id)
# or
members = group.members.get(member_id)
# end member get

# member create
member = gl.group_members.create({'user_id': user_id,
                                  'access_level': gitlab.GUEST_ACCESS},
                                 group_id=1)
# or
member = group.members.create({'user_id': user_id,
                               'access_level': gitlab.GUEST_ACCESS})
# end member create

# member update
member.access_level = gitlab.DEVELOPER_ACCESS
member.save()
# end member update

# member delete
gl.group_members.delete(member_id, group_id=1)
# or
group.members.delete(member_id)
# or
member.delete()
# end member delete

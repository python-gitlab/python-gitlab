# list
branches = project.branches.list()
# end list

# get
branch = project.branches.get('master')
# end get

# create
# v4
branch = project.branches.create({'branch': 'feature1',
                                  'ref': 'master'})

#v3
branch = project.branches.create({'branch_name': 'feature1',
                                  'ref': 'master'})
# end create

# delete
project.branches.delete('feature1')
# or
branch.delete()
# end delete

# protect
branch.protect()
branch.unprotect()
# end protect

# p_branch list
p_branches = project.protectedbranches.list()
# end p_branch list

# p_branch get
p_branch = project.protectedbranches.get('master')
# end p_branch get

# p_branch create
p_branch = project.protectedbranches.create({'name': '*-stable'})
# end p_branch create

# p_branch delete
project.protectedbranches.delete('*-stable')
# or
p_branch.delete()
# end p_branch delete

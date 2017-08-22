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

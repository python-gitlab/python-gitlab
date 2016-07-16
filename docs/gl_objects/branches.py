# list
branches = gl.project_branches.list(project_id=1)
# or
branches = project.branches.list()
# end list

# get
branch = gl.project_branches.get(project_id=1, id='master')
# or
branch = project.branches.get('master')
# end get

# create
branch = gl.project_branches.create({'branch_name': 'feature1',
                                     'ref': 'master'},
                                    project_id=1)
# or
branch = project.branches.create({'branch_name': 'feature1',
                                  'ref': 'master'})
# end create

# delete
gl.project_branches.delete(project_id=1, id='feature1')
# or
project.branches.delete('feature1')
# or
branch.delete()
# end delete

# protect
branch.protect()
branch.unprotect()
# end protect

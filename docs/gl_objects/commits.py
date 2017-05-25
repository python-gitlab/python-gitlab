# list
commits = gl.project_commits.list(project_id=1)
# or
commits = project.commits.list()
# end list

# filter list
commits = project.commits.list(ref_name='my_branch')
commits = project.commits.list(since='2016-01-01T00:00:00Z')
# end filter list

# create
# See https://docs.gitlab.com/ce/api/commits.html#create-a-commit-with-multiple-files-and-actions
# for actions detail
data = {
    'branch_name': 'master',
    'commit_message': 'blah blah blah',
    'actions': [
        {
            'action': 'create',
            'file_path': 'blah',
            'content': 'blah'
        }
    ]
}

commit = gl.project_commits.create(data, project_id=1)
# or
commit = project.commits.create(data)
# end create

# get
commit = gl.project_commits.get('e3d5a71b', project_id=1)
# or
commit = project.commits.get('e3d5a71b')
# end get

# diff
diff = commit.diff()
# end diff

# cherry
commit.cherry_pick(branch='target_branch')
# end cherry

# comments list
comments = gl.project_commit_comments.list(project_id=1, commit_id='master')
# or
comments = project.commit_comments.list(commit_id='a5fe4c8')
# or
comments = commit.comments.list()
# end comments list

# comments create
# Global comment
commit = commit.comments.create({'note': 'This is a nice comment'})
# Comment on a line in a file (on the new version of the file)
commit = commit.comments.create({'note': 'This is another comment',
                                 'line': 12,
                                 'line_type': 'new',
                                 'path': 'README.rst'})
# end comments create

# statuses list
statuses = gl.project_commit_statuses.list(project_id=1, commit_id='master')
# or
statuses = project.commit_statuses.list(commit_id='a5fe4c8')
# or
statuses = commit.statuses.list()
# end statuses list

# statuses set
commit.statuses.create({'state': 'success'})
# end statuses set

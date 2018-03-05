# list
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
    'branch_name': 'master',  # v3
    'branch': 'master',  # v4
    'commit_message': 'blah blah blah',
    'actions': [
        {
            'action': 'create',
            'file_path': 'README.rst',
            'content': open('path/to/file.rst').read(),
        },
        {
            # Binary files need to be base64 encoded
            'action': 'create',
            'file_path': 'logo.png',
            'content': base64.b64encode(open('logo.png').read()),
            'encoding': 'base64',
        }
    ]
}

commit = project.commits.create(data)
# end create

# get
commit = project.commits.get('e3d5a71b')
# end get

# diff
diff = commit.diff()
# end diff

# cherry
commit.cherry_pick(branch='target_branch')
# end cherry

# comments list
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
statuses = commit.statuses.list()
# end statuses list

# statuses set
commit.statuses.create({'state': 'success'})
# end statuses set

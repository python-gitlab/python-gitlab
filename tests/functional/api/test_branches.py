"""
GitLab API:
https://docs.gitlab.com/ee/api/branches.html
"""


def test_branch_name_with_period(project):
    # Make sure we can create and get a branch name containing a period '.'
    branch_name = "my.branch.name"
    branch = project.branches.create(
        {"branch": branch_name, "ref": "main", "default": True}
    )
    assert branch.name == branch_name
    assert branch.default is True

    # Ensure we can get the branch
    fetched_branch = project.branches.get(branch_name)
    assert branch.name == fetched_branch.name
    assert branch.default == fetched_branch.default

    branch.delete()

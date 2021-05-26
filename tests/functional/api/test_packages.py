"""
GitLab API: https://docs.gitlab.com/ce/api/packages.html
"""


def test_list_project_packages(project):
    packages = project.packages.list()
    assert isinstance(packages, list)


def test_list_group_packages(group):
    packages = group.packages.list()
    assert isinstance(packages, list)

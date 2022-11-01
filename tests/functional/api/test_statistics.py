"""
GitLab API: https://docs.gitlab.com/ee/api/statistics.html
"""


def test_get_statistics(gl):
    statistics = gl.statistics.get()

    assert statistics.snippets.isdigit()
    assert statistics.users.isdigit()
    assert statistics.groups.isdigit()
    assert statistics.projects.isdigit()

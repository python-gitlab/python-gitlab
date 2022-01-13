"""
GitLab API:
https://docs.gitlab.com/ee/api/integrations.html
"""

import gitlab


def test_services(project):
    service = project.services.get("jira", lazy=True)
    assert isinstance(service, gitlab.v4.objects.ProjectService)

"""
Gitlab API:
https://docs.gitlab.com/ce/api/templates/dockerfiles.html
https://docs.gitlab.com/ce/api/templates/gitignores.html
https://docs.gitlab.com/ce/api/templates/gitlab_ci_ymls.html
https://docs.gitlab.com/ce/api/templates/licenses.html
https://docs.gitlab.com/ce/api/project_templates.html
"""

import pytest
import responses

from gitlab.v4.objects import (
    Dockerfile,
    Gitignore,
    Gitlabciyml,
    License,
    ProjectDockerfileTemplate,
    ProjectGitignoreTemplate,
    ProjectGitlabciymlTemplate,
    ProjectIssueTemplate,
    ProjectLicenseTemplate,
    ProjectMergeRequestTemplate,
)


@pytest.mark.parametrize(
    "fixture, tmpl, tmpl_path, tmpl_mgr",
    [
        ("gl", Dockerfile, "dockerfiles", "dockerfiles"),
        ("gl", Gitignore, "gitignores", "gitignores"),
        ("gl", Gitlabciyml, "gitlab_ci_ymls", "gitlabciymls"),
        ("gl", License, "licenses", "licenses"),
        ("project", ProjectDockerfileTemplate, "dockerfiles", "dockerfile_templates"),
        ("project", ProjectGitignoreTemplate, "gitignores", "gitignore_templates"),
        (
            "project",
            ProjectGitlabciymlTemplate,
            "gitlab_ci_ymls",
            "gitlabciyml_templates",
        ),
        ("project", ProjectLicenseTemplate, "licenses", "license_templates"),
        ("project", ProjectIssueTemplate, "issues", "issue_templates"),
        (
            "project",
            ProjectMergeRequestTemplate,
            "merge_requests",
            "mergerequest_templates",
        ),
    ],
    ids=[
        "dockerfile",
        "gitignore",
        "gitlabciyml",
        "license",
        "project_dockerfile",
        "project_gitignore",
        "project_gitlabciyml",
        "project_license",
        "project_issue",
        "project_mergerequest",
    ],
)
def test_get_template(request, fixture, tmpl, tmpl_path, tmpl_mgr):
    # Get the appropriate fixture and path. `owner` is the object that
    # aggregates the template managers, i.e., Gitlab, Project
    owner = request.getfixturevalue(fixture)
    owner_path = "/" if fixture == "gl" else f"/projects/{owner.id}/"

    tmpl_id = "sample"
    tmpl_content = {"name": tmpl_id, "content": "Sample template content"}

    # License templates have 'key' as the id attribute, so ensure
    # this is included in the response content
    if tmpl == License or tmpl == ProjectLicenseTemplate:
        tmpl_id = "smpl"
        tmpl_content.update({"key": tmpl_id})

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=f"http://localhost/api/v4{owner_path}templates/{tmpl_path}/{tmpl_id}",
            json=tmpl_content,
        )

        template = getattr(owner, tmpl_mgr).get(tmpl_id)

    assert isinstance(template, tmpl)
    assert getattr(template, template._id_attr) == tmpl_id

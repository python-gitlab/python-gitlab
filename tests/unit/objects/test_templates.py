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
    "tmpl, tmpl_mgr, tmpl_path",
    [
        (Dockerfile, "dockerfiles", "dockerfiles"),
        (Gitignore, "gitignores", "gitignores"),
        (Gitlabciyml, "gitlabciymls", "gitlab_ci_ymls"),
        (License, "licenses", "licenses"),
    ],
    ids=[
        "dockerfile",
        "gitignore",
        "gitlabciyml",
        "license",
    ],
)
def test_get_template(gl, tmpl, tmpl_mgr, tmpl_path):
    tmpl_id = "sample"
    tmpl_content = {"name": tmpl_id, "content": "Sample template content"}

    # License templates have 'key' as the id attribute, so ensure
    # this is included in the response content
    if tmpl == License:
        tmpl_id = "smpl"
        tmpl_content.update({"key": tmpl_id})

    path = f"templates/{tmpl_path}/{tmpl_id}"
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=f"http://localhost/api/v4/{path}",
            json=tmpl_content,
        )

        template = getattr(gl, tmpl_mgr).get(tmpl_id)

    assert isinstance(template, tmpl)
    assert getattr(template, template._id_attr) == tmpl_id


@pytest.mark.parametrize(
    "tmpl, tmpl_mgr, tmpl_path",
    [
        (ProjectDockerfileTemplate, "dockerfile_templates", "dockerfiles"),
        (ProjectGitignoreTemplate, "gitignore_templates", "gitignores"),
        (ProjectGitlabciymlTemplate, "gitlabciyml_templates", "gitlab_ci_ymls"),
        (ProjectLicenseTemplate, "license_templates", "licenses"),
        (ProjectIssueTemplate, "issue_templates", "issues"),
        (ProjectMergeRequestTemplate, "merge_request_templates", "merge_requests"),
    ],
    ids=[
        "dockerfile",
        "gitignore",
        "gitlabciyml",
        "license",
        "issue",
        "mergerequest",
    ],
)
def test_get_project_template(project, tmpl, tmpl_mgr, tmpl_path):
    tmpl_id = "sample"
    tmpl_content = {"name": tmpl_id, "content": "Sample template content"}

    # ProjectLicenseTemplate templates have 'key' as the id attribute, so ensure
    # this is included in the response content
    if tmpl == ProjectLicenseTemplate:
        tmpl_id = "smpl"
        tmpl_content.update({"key": tmpl_id})

    path = f"projects/{project.id}/templates/{tmpl_path}/{tmpl_id}"
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=f"http://localhost/api/v4/{path}",
            json=tmpl_content,
        )

        template = getattr(project, tmpl_mgr).get(tmpl_id)

    assert isinstance(template, tmpl)
    assert getattr(template, template._id_attr) == tmpl_id

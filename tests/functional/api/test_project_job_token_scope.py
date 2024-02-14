import pytest


# TODO: can be enabled when https://github.com/python-gitlab/python-gitlab/pull/2790 merged
@pytest.mark.xfail(reason="project job_token_scope api only in 16.*")
def test_add_project_to_job_token_scope_allowlist(gl, project):
    project_to_add = gl.projects.create({"name": "Ci_Cd_token_add_proj"})

    scope = project.job_token_scope.get()
    resp = scope.allowlist.create({"target_project_id": project_to_add.id})

    assert resp.source_project_id == project.id
    assert resp.target_project_id == project_to_add.id

    project_to_add.delete()


@pytest.mark.xfail(reason="project job_token_scope api only in 16.*")
def test_projects_job_token_scope_allowlist_contains_added_project_name(gl, project):
    scope = project.job_token_scope.get()
    assert len(scope.allowlist.list()) == 0

    project_name = "Ci_Cd_token_named_proj"
    project_to_add = gl.projects.create({"name": project_name})
    scope.allowlist.create({"target_project_id": project_to_add.id})

    scope.refresh()
    assert any(allowed.name == project_name for allowed in scope.allowlist.list())

    project_to_add.delete()


@pytest.mark.xfail(reason="project job_token_scope api only in 16.*")
def test_remove_project_by_id_from_projects_job_token_scope_allowlist(gl, project):
    scope = project.job_token_scope.get()
    assert len(scope.allowlist.list()) == 0

    project_to_add = gl.projects.create({"name": "Ci_Cd_token_remove_proj"})

    scope.allowlist.create({"target_project_id": project_to_add.id})

    scope.refresh()
    assert len(scope.allowlist.list()) != 0

    scope.allowlist.remove(project_to_add.id)

    scope.refresh()
    assert len(scope.allowlist.list()) == 0

    project_to_add.delete()

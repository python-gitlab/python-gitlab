# https://docs.gitlab.com/ee/ci/jobs/ci_job_token.html#allow-any-project-to-access-your-project
def test_enable_limit_access_to_this_project(gl, project):
    scope = project.job_token_scope.get()

    scope.enabled = True
    scope.save()

    scope.refresh()

    assert scope.inbound_enabled


def test_disable_limit_access_to_this_project(gl, project):
    scope = project.job_token_scope.get()

    scope.enabled = False
    scope.save()

    scope.refresh()

    assert not scope.inbound_enabled


def test_add_project_to_job_token_scope_allowlist(gl, project):
    project_to_add = gl.projects.create({"name": "Ci_Cd_token_add_proj"})

    scope = project.job_token_scope.get()
    resp = scope.allowlist.create({"target_project_id": project_to_add.id})

    assert resp.source_project_id == project.id
    assert resp.target_project_id == project_to_add.id

    project_to_add.delete()


def test_projects_job_token_scope_allowlist_contains_added_project_name(gl, project):
    scope = project.job_token_scope.get()
    project_name = "Ci_Cd_token_named_proj"
    project_to_add = gl.projects.create({"name": project_name})
    scope.allowlist.create({"target_project_id": project_to_add.id})

    scope.refresh()
    assert any(allowed.name == project_name for allowed in scope.allowlist.list())

    project_to_add.delete()


def test_remove_project_by_id_from_projects_job_token_scope_allowlist(gl, project):
    scope = project.job_token_scope.get()

    project_to_add = gl.projects.create({"name": "Ci_Cd_token_remove_proj"})

    scope.allowlist.create({"target_project_id": project_to_add.id})

    scope.refresh()

    scope.allowlist.delete(project_to_add.id)

    scope.refresh()
    assert not any(
        allowed.id == project_to_add.id for allowed in scope.allowlist.list()
    )

    project_to_add.delete()


def test_add_group_to_job_token_scope_allowlist(gl, project):
    group_to_add = gl.groups.create(
        {"name": "add_group", "path": "allowlisted-add-test"}
    )

    scope = project.job_token_scope.get()
    resp = scope.groups_allowlist.create({"target_group_id": group_to_add.id})

    assert resp.source_project_id == project.id
    assert resp.target_group_id == group_to_add.id

    group_to_add.delete()


def test_projects_job_token_scope_groups_allowlist_contains_added_group_name(
    gl, project
):
    scope = project.job_token_scope.get()
    group_name = "list_group"
    group_to_add = gl.groups.create(
        {"name": group_name, "path": "allowlisted-add-and-list-test"}
    )

    scope.groups_allowlist.create({"target_group_id": group_to_add.id})

    scope.refresh()
    assert any(allowed.name == group_name for allowed in scope.groups_allowlist.list())

    group_to_add.delete()


def test_remove_group_by_id_from_projects_job_token_scope_groups_allowlist(gl, project):
    scope = project.job_token_scope.get()

    group_to_add = gl.groups.create(
        {"name": "delete_group", "path": "allowlisted-delete-test"}
    )

    scope.groups_allowlist.create({"target_group_id": group_to_add.id})

    scope.refresh()

    scope.groups_allowlist.delete(group_to_add.id)

    scope.refresh()
    assert not any(
        allowed.name == group_to_add.name for allowed in scope.groups_allowlist.list()
    )

    group_to_add.delete()

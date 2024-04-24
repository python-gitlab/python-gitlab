import datetime
import os
import time

branch = "BRANCH-cli-v4"


def test_create_project(gitlab_cli):
    name = "test-project1"

    cmd = ["project", "create", "--name", name]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert name in ret.stdout


def test_update_project(gitlab_cli, project):
    description = "My New Description"

    cmd = ["project", "update", "--id", project.id, "--description", description]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert description in ret.stdout


def test_validate_project_ci_lint(gitlab_cli, project, valid_gitlab_ci_yml):
    cmd = [
        "project-ci-lint",
        "validate",
        "--project-id",
        project.id,
        "--content",
        valid_gitlab_ci_yml,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_validate_project_ci_lint_invalid_exits_non_zero(
    gitlab_cli, project, invalid_gitlab_ci_yml
):
    cmd = [
        "project-ci-lint",
        "validate",
        "--project-id",
        project.id,
        "--content",
        invalid_gitlab_ci_yml,
    ]
    ret = gitlab_cli(cmd)

    assert not ret.success
    assert "CI YAML Lint failed (Invalid configuration format)" in ret.stderr


def test_create_group(gitlab_cli):
    name = "test-group1"
    path = "group1"

    cmd = ["group", "create", "--name", name, "--path", path]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert name in ret.stdout
    assert path in ret.stdout


def test_update_group(gitlab_cli, gl, group):
    description = "My New Description"

    cmd = ["group", "update", "--id", group.id, "--description", description]
    ret = gitlab_cli(cmd)

    assert ret.success

    group = gl.groups.get(group.id)
    assert group.description == description


def test_create_user(gitlab_cli, gl):
    email = "fake@email.com"
    username = "user1"
    name = "User One"
    password = "E4596f8be406Bc3a14a4ccdb1df80587"

    cmd = [
        "user",
        "create",
        "--email",
        email,
        "--username",
        username,
        "--name",
        name,
        "--password",
        password,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success

    user = gl.users.list(username=username)[0]

    assert user.email == email
    assert user.username == username
    assert user.name == name


def test_get_user_by_id(gitlab_cli, user):
    cmd = ["user", "get", "--id", user.id]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert str(user.id) in ret.stdout


def test_list_users_verbose_output(gitlab_cli):
    cmd = ["-v", "user", "list"]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert "avatar-url" in ret.stdout


def test_cli_args_not_in_output(gitlab_cli):
    cmd = ["-v", "user", "list"]
    ret = gitlab_cli(cmd)

    assert "config-file" not in ret.stdout


def test_add_member_to_project(gitlab_cli, project, user):
    access_level = "40"

    cmd = [
        "project-member",
        "create",
        "--project-id",
        project.id,
        "--user-id",
        user.id,
        "--access-level",
        access_level,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_user_memberships(gitlab_cli, user):
    cmd = ["user-membership", "list", "--user-id", user.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_project_issue(gitlab_cli, project):
    title = "my issue"
    description = "my issue description"

    cmd = [
        "project-issue",
        "create",
        "--project-id",
        project.id,
        "--title",
        title,
        "--description",
        description,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert title in ret.stdout


def test_create_issue_note(gitlab_cli, issue):
    body = "body"

    cmd = [
        "project-issue-note",
        "create",
        "--project-id",
        issue.project_id,
        "--issue-iid",
        issue.iid,
        "--body",
        body,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_branch(gitlab_cli, project):
    cmd = [
        "project-branch",
        "create",
        "--project-id",
        project.id,
        "--branch",
        branch,
        "--ref",
        "main",
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_merge_request(gitlab_cli, project):

    cmd = [
        "project-merge-request",
        "create",
        "--project-id",
        project.id,
        "--source-branch",
        branch,
        "--target-branch",
        "main",
        "--title",
        "Update README",
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_accept_request_merge(gitlab_cli, project):
    # MR needs at least 1 commit before we can merge
    mr = project.mergerequests.list()[0]
    file_data = {
        "branch": mr.source_branch,
        "file_path": "test-cli-v4.md",
        "content": "Content",
        "commit_message": "chore: test-cli-v4 change",
    }
    project.files.create(file_data)
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(30)

    approve_cmd = [
        "project-merge-request",
        "merge",
        "--project-id",
        project.id,
        "--iid",
        mr.iid,
    ]
    ret = gitlab_cli(approve_cmd)

    assert ret.success


def test_create_project_label(gitlab_cli, project):
    name = "prjlabel1"
    description = "prjlabel1 description"
    color = "#112233"

    cmd = [
        "-v",
        "project-label",
        "create",
        "--project-id",
        project.id,
        "--name",
        name,
        "--description",
        description,
        "--color",
        color,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_project_labels(gitlab_cli, project):
    cmd = ["-v", "project-label", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_update_project_label(gitlab_cli, label):
    new_label = "prjlabel2"
    new_description = "prjlabel2 description"
    new_color = "#332211"

    cmd = [
        "-v",
        "project-label",
        "update",
        "--project-id",
        label.project_id,
        "--name",
        label.name,
        "--new-name",
        new_label,
        "--description",
        new_description,
        "--color",
        new_color,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_delete_project_label(gitlab_cli, label):
    # TODO: due to update above, we'd need a function-scope label fixture
    label_name = "prjlabel2"

    cmd = [
        "-v",
        "project-label",
        "delete",
        "--project-id",
        label.project_id,
        "--name",
        label_name,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_group_label(gitlab_cli, group):
    name = "grouplabel1"
    description = "grouplabel1 description"
    color = "#112233"

    cmd = [
        "-v",
        "group-label",
        "create",
        "--group-id",
        group.id,
        "--name",
        name,
        "--description",
        description,
        "--color",
        color,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_group_labels(gitlab_cli, group):
    cmd = ["-v", "group-label", "list", "--group-id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_update_group_label(gitlab_cli, group_label):
    new_label = "grouplabel2"
    new_description = "grouplabel2 description"
    new_color = "#332211"

    cmd = [
        "-v",
        "group-label",
        "update",
        "--group-id",
        group_label.group_id,
        "--name",
        group_label.name,
        "--new-name",
        new_label,
        "--description",
        new_description,
        "--color",
        new_color,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_delete_group_label(gitlab_cli, group_label):
    # TODO: due to update above, we'd need a function-scope label fixture
    new_label = "grouplabel2"

    cmd = [
        "-v",
        "group-label",
        "delete",
        "--group-id",
        group_label.group_id,
        "--name",
        new_label,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_project_variable(gitlab_cli, project):
    key = "junk"
    value = "car"

    cmd = [
        "-v",
        "project-variable",
        "create",
        "--project-id",
        project.id,
        "--key",
        key,
        "--value",
        value,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_get_project_variable(gitlab_cli, variable):
    cmd = [
        "-v",
        "project-variable",
        "get",
        "--project-id",
        variable.project_id,
        "--key",
        variable.key,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_update_project_variable(gitlab_cli, variable):
    new_value = "bus"

    cmd = [
        "-v",
        "project-variable",
        "update",
        "--project-id",
        variable.project_id,
        "--key",
        variable.key,
        "--value",
        new_value,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_project_variables(gitlab_cli, project):
    cmd = ["-v", "project-variable", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_delete_project_variable(gitlab_cli, variable):
    cmd = [
        "-v",
        "project-variable",
        "delete",
        "--project-id",
        variable.project_id,
        "--key",
        variable.key,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_delete_branch(gitlab_cli, project):
    cmd = ["project-branch", "delete", "--project-id", project.id, "--name", branch]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_project_upload_file(gitlab_cli, project):
    cmd = [
        "project",
        "upload",
        "--id",
        project.id,
        "--filename",
        __file__,
        "--filepath",
        os.path.realpath(__file__),
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_get_application_settings(gitlab_cli):
    cmd = ["application-settings", "get"]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_update_application_settings(gitlab_cli):
    cmd = ["application-settings", "update", "--signup-enabled", "false"]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_create_project_with_values_from_file(gitlab_cli, fixture_dir, tmpdir):
    name = "gitlab-project-from-file"
    description = "Multiline\n\nData\n"
    from_file = tmpdir.join(name)
    from_file.write(description)
    from_file_path = f"@{str(from_file)}"
    avatar_file = fixture_dir / "avatar.png"
    assert avatar_file.exists()
    avatar_file_path = f"@{avatar_file}"

    cmd = [
        "-v",
        "project",
        "create",
        "--name",
        name,
        "--description",
        from_file_path,
        "--avatar",
        avatar_file_path,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert description in ret.stdout


def test_create_project_with_values_at_prefixed(gitlab_cli, tmpdir):
    name = "gitlab-project-at-prefixed"
    description = "@at-prefixed"
    at_prefixed = f"@{description}"

    cmd = [
        "-v",
        "project",
        "create",
        "--name",
        name,
        "--description",
        at_prefixed,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert description in ret.stdout


def test_create_project_deploy_token(gitlab_cli, project):
    name = "project-token"
    username = "root"
    expires_at = datetime.date.today().isoformat()
    scopes = "read_registry"

    cmd = [
        "-v",
        "project-deploy-token",
        "create",
        "--project-id",
        project.id,
        "--name",
        name,
        "--username",
        username,
        "--expires-at",
        expires_at,
        "--scopes",
        scopes,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert name in ret.stdout
    assert username in ret.stdout
    assert expires_at in ret.stdout
    assert scopes in ret.stdout


def test_list_all_deploy_tokens(gitlab_cli, deploy_token):
    cmd = ["-v", "deploy-token", "list"]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert deploy_token.name in ret.stdout
    assert str(deploy_token.id) in ret.stdout
    assert deploy_token.username in ret.stdout
    assert deploy_token.expires_at in ret.stdout
    assert deploy_token.scopes[0] in ret.stdout


def test_list_project_deploy_tokens(gitlab_cli, deploy_token):
    cmd = [
        "-v",
        "project-deploy-token",
        "list",
        "--project-id",
        deploy_token.project_id,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert deploy_token.name in ret.stdout
    assert str(deploy_token.id) in ret.stdout
    assert deploy_token.username in ret.stdout
    assert deploy_token.expires_at in ret.stdout
    assert deploy_token.scopes[0] in ret.stdout


def test_delete_project_deploy_token(gitlab_cli, deploy_token):
    cmd = [
        "-v",
        "project-deploy-token",
        "delete",
        "--project-id",
        deploy_token.project_id,
        "--id",
        deploy_token.id,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    # TODO assert not in list


def test_create_group_deploy_token(gitlab_cli, group):
    name = "group-token"
    username = "root"
    expires_at = datetime.date.today().isoformat()
    scopes = "read_registry"

    cmd = [
        "-v",
        "group-deploy-token",
        "create",
        "--group-id",
        group.id,
        "--name",
        name,
        "--username",
        username,
        "--expires-at",
        expires_at,
        "--scopes",
        scopes,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert name in ret.stdout
    assert username in ret.stdout
    assert expires_at in ret.stdout
    assert scopes in ret.stdout


def test_list_group_deploy_tokens(gitlab_cli, group_deploy_token):
    cmd = [
        "-v",
        "group-deploy-token",
        "list",
        "--group-id",
        group_deploy_token.group_id,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    assert group_deploy_token.name in ret.stdout
    assert str(group_deploy_token.id) in ret.stdout
    assert group_deploy_token.username in ret.stdout
    assert group_deploy_token.expires_at in ret.stdout
    assert group_deploy_token.scopes[0] in ret.stdout


def test_delete_group_deploy_token(gitlab_cli, group_deploy_token):
    cmd = [
        "-v",
        "group-deploy-token",
        "delete",
        "--group-id",
        group_deploy_token.group_id,
        "--id",
        group_deploy_token.id,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success
    # TODO assert not in list


def test_project_member_all(gitlab_cli, project):
    cmd = [
        "project-member-all",
        "list",
        "--project-id",
        project.id,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_group_member_all(gitlab_cli, group):
    cmd = [
        "group-member-all",
        "list",
        "--group-id",
        group.id,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


# Deleting the project and group. Add your tests above here.
def test_delete_project(gitlab_cli, project):
    cmd = ["project", "delete", "--id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_delete_group(gitlab_cli, group):
    cmd = ["group", "delete", "--id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success


# Don't add tests below here as the group and project have been deleted

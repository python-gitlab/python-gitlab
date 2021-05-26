def test_project_deploy_tokens(gl, project):
    deploy_token = project.deploytokens.create(
        {
            "name": "foo",
            "username": "bar",
            "expires_at": "2022-01-01",
            "scopes": ["read_registry"],
        }
    )
    assert len(project.deploytokens.list()) == 1
    assert gl.deploytokens.list() == project.deploytokens.list()

    assert project.deploytokens.list()[0].name == "foo"
    assert project.deploytokens.list()[0].expires_at == "2022-01-01T00:00:00.000Z"
    assert project.deploytokens.list()[0].scopes == ["read_registry"]
    assert project.deploytokens.list()[0].username == "bar"

    deploy_token.delete()
    assert len(project.deploytokens.list()) == 0
    assert len(gl.deploytokens.list()) == 0


def test_group_deploy_tokens(gl, group):
    deploy_token = group.deploytokens.create(
        {
            "name": "foo",
            "scopes": ["read_registry"],
        }
    )

    assert len(group.deploytokens.list()) == 1
    assert gl.deploytokens.list() == group.deploytokens.list()

    deploy_token.delete()
    assert len(group.deploytokens.list()) == 0
    assert len(gl.deploytokens.list()) == 0

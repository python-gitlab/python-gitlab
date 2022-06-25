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

    deploy_token = project.deploytokens.get(deploy_token.id)
    assert deploy_token.name == "foo"
    assert deploy_token.expires_at == "2022-01-01T00:00:00.000Z"
    assert deploy_token.scopes == ["read_registry"]
    assert deploy_token.username == "bar"

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

    deploy_token = group.deploytokens.get(deploy_token.id)
    assert deploy_token.name == "foo"
    assert deploy_token.scopes == ["read_registry"]

    deploy_token.delete()
    assert len(group.deploytokens.list()) == 0
    assert len(gl.deploytokens.list()) == 0

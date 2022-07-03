def test_project_deploy_tokens(gl, project):
    deploy_token = project.deploytokens.create(
        {
            "name": "foo",
            "username": "bar",
            "expires_at": "2022-01-01",
            "scopes": ["read_registry"],
        }
    )
    assert deploy_token in project.deploytokens.list()
    assert set(project.deploytokens.list()) <= set(gl.deploytokens.list())

    deploy_token = project.deploytokens.get(deploy_token.id)
    assert deploy_token.name == "foo"
    assert deploy_token.expires_at == "2022-01-01T00:00:00.000Z"
    assert deploy_token.scopes == ["read_registry"]
    assert deploy_token.username == "bar"

    deploy_token.delete()
    assert deploy_token not in project.deploytokens.list()
    assert deploy_token not in gl.deploytokens.list()


def test_group_deploy_tokens(gl, group):
    deploy_token = group.deploytokens.create(
        {
            "name": "foo",
            "scopes": ["read_registry"],
        }
    )

    assert deploy_token in group.deploytokens.list()
    assert set(group.deploytokens.list()) <= set(gl.deploytokens.list())

    deploy_token = group.deploytokens.get(deploy_token.id)
    assert deploy_token.name == "foo"
    assert deploy_token.scopes == ["read_registry"]

    deploy_token.delete()
    assert deploy_token not in group.deploytokens.list()
    assert deploy_token not in gl.deploytokens.list()

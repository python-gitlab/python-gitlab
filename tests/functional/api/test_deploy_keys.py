def test_project_deploy_keys(gl, project, DEPLOY_KEY):
    deploy_key = project.keys.create({"title": "foo@bar", "key": DEPLOY_KEY})
    project_keys = list(project.keys.list())
    assert len(project_keys) == 1

    project2 = gl.projects.create({"name": "deploy-key-project"})
    project2.keys.enable(deploy_key.id)
    assert len(project2.keys.list()) == 1

    project2.keys.delete(deploy_key.id)
    assert len(project2.keys.list()) == 0
    project2.delete()

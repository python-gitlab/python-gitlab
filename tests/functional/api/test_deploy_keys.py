def test_project_deploy_keys(gl, project, DEPLOY_KEY):
    deploy_key = project.keys.create({"title": "foo@bar", "key": DEPLOY_KEY})
    assert deploy_key in project.keys.list()

    project2 = gl.projects.create({"name": "deploy-key-project"})
    project2.keys.enable(deploy_key.id)
    assert deploy_key in project2.keys.list()

    project2.keys.delete(deploy_key.id)

    project2.delete()

from gitlab import Gitlab
from gitlab.v4.objects import Project


def test_deploy_keys(gl: Gitlab, DEPLOY_KEY: str) -> None:
    deploy_key = gl.deploykeys.create({"title": "foo@bar", "key": DEPLOY_KEY})
    assert deploy_key in gl.deploykeys.list(get_all=False)


def test_project_deploy_keys(gl: Gitlab, project: Project, DEPLOY_KEY: str) -> None:
    deploy_key = project.keys.create({"title": "foo@bar", "key": DEPLOY_KEY})
    assert deploy_key in project.keys.list()

    project2 = gl.projects.create({"name": "deploy-key-project"})
    project2.keys.enable(deploy_key.id)
    assert deploy_key in project2.keys.list()

    project2.keys.delete(deploy_key.id)

    project2.delete()

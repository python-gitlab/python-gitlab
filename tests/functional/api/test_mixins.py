import pytest


@pytest.fixture
def lazy_project(gl, project):
    return gl.projects.get(project.path_with_namespace, lazy=True)


def test_refresh_after_lazy_get_with_path(project, lazy_project):
    lazy_project.refresh()
    assert lazy_project.id == project.id


def test_save_after_lazy_get_with_path(project, lazy_project):
    lazy_project.description = "A new description"
    lazy_project.save()
    assert lazy_project.id == project.id
    assert lazy_project.description == "A new description"


@pytest.mark.xfail(reason="See #1494")
def test_delete_after_lazy_get_with_path(gl, lazy_project):
    lazy_project.delete()

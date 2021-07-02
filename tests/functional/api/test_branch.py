import gitlab
import pytest

@pytest.mark.parametrize("lazy", [True, False])
def test_delete_branch(gl, project, branch, lazy):
    b = project.branches.get(branch.name, lazy=lazy)
    b.delete()

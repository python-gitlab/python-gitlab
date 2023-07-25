"""
GitLab API:
https://docs.gitlab.com/ee/api/instance_level_ci_variables.html
https://docs.gitlab.com/ee/api/project_level_variables.html
https://docs.gitlab.com/ee/api/group_level_variables.html
"""

import re

import pytest
import responses

from gitlab.v4.objects import GroupVariable, ProjectVariable, Variable

key = "TEST_VARIABLE_1"
value = "TEST_1"
new_value = "TEST_2"

variable_content = {
    "key": key,
    "variable_type": "env_var",
    "value": value,
    "protected": False,
    "masked": True,
}
variables_url = re.compile(
    r"http://localhost/api/v4/(((groups|projects)/1)|(admin/ci))/variables"
)
variables_key_url = re.compile(
    rf"http://localhost/api/v4/(((groups|projects)/1)|(admin/ci))/variables/{key}"
)


@pytest.fixture
def resp_list_variables():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=variables_url,
            json=[variable_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_variable():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=variables_key_url,
            json=variable_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_variable():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=variables_url,
            json=variable_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_update_variable():
    updated_content = dict(variable_content)
    updated_content["value"] = new_value

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url=variables_key_url,
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_variable():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url=variables_key_url,
            status=204,
        )
        yield rsps


def test_list_instance_variables(gl, resp_list_variables):
    variables = gl.variables.list()
    assert isinstance(variables, list)
    assert isinstance(variables[0], Variable)
    assert variables[0].value == value


def test_get_instance_variable(gl, resp_get_variable):
    variable = gl.variables.get(key)
    assert isinstance(variable, Variable)
    assert variable.value == value


def test_create_instance_variable(gl, resp_create_variable):
    variable = gl.variables.create({"key": key, "value": value})
    assert isinstance(variable, Variable)
    assert variable.value == value


def test_update_instance_variable(gl, resp_update_variable):
    variable = gl.variables.get(key, lazy=True)
    variable.value = new_value
    variable.save()
    assert variable.value == new_value


def test_delete_instance_variable(gl, resp_delete_variable):
    variable = gl.variables.get(key, lazy=True)
    variable.delete()


def test_list_project_variables(project, resp_list_variables):
    variables = project.variables.list()
    assert isinstance(variables, list)
    assert isinstance(variables[0], ProjectVariable)
    assert variables[0].value == value


def test_get_project_variable(project, resp_get_variable):
    variable = project.variables.get(key)
    assert isinstance(variable, ProjectVariable)
    assert variable.value == value


def test_create_project_variable(project, resp_create_variable):
    variable = project.variables.create({"key": key, "value": value})
    assert isinstance(variable, ProjectVariable)
    assert variable.value == value


def test_update_project_variable(project, resp_update_variable):
    variable = project.variables.get(key, lazy=True)
    variable.value = new_value
    variable.save()
    assert variable.value == new_value


def test_delete_project_variable(project, resp_delete_variable):
    variable = project.variables.get(key, lazy=True)
    variable.delete()


def test_list_group_variables(group, resp_list_variables):
    variables = group.variables.list()
    assert isinstance(variables, list)
    assert isinstance(variables[0], GroupVariable)
    assert variables[0].value == value


def test_get_group_variable(group, resp_get_variable):
    variable = group.variables.get(key)
    assert isinstance(variable, GroupVariable)
    assert variable.value == value


def test_create_group_variable(group, resp_create_variable):
    variable = group.variables.create({"key": key, "value": value})
    assert isinstance(variable, GroupVariable)
    assert variable.value == value


def test_update_group_variable(group, resp_update_variable):
    variable = group.variables.get(key, lazy=True)
    variable.value = new_value
    variable.save()
    assert variable.value == new_value


def test_delete_group_variable(group, resp_delete_variable):
    variable = group.variables.get(key, lazy=True)
    variable.delete()

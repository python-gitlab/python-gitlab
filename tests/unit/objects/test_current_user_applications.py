"""
GitLab API: https://docs.gitlab.com/api/user_applications
"""

import pytest
import responses

from gitlab.v4.objects import CurrentUserApplication

application_content = {
    "id": 1,
    "application_id": "5832fc6e14300a0d962240a8144466eef4ee93ef",
    "application_name": "MyApplication",
    "callback_url": "http://redirect.uri",
    "confidential": True,
}
updated_content = {**application_content, "application_name": "UpdatedApplication"}


@pytest.fixture
def resp_create_application():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/user/applications",
            json={**application_content, "secret": "secret"},
            content_type="application/json",
            status=201,
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "name": "MyApplication",
                        "redirect_uri": "http://redirect.uri",
                        "scopes": "api read_user",
                        "confidential": True,
                    }
                )
            ],
        )
        yield rsps


@pytest.fixture
def resp_list_application():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/user/applications",
            json=[application_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_application():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/user/applications/1",
            json=application_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_update_application():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/user/applications/1",
            json=application_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/user/applications/1",
            json=updated_content,
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.json_params_matcher({"name": "UpdatedApplication"})
            ],
        )
        yield rsps


@pytest.fixture
def resp_delete_application():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/user/applications/1",
            status=204,
        )
        yield rsps


def test_create_current_user_application(current_user, resp_create_application):
    application = current_user.applications.create(
        {
            "name": "MyApplication",
            "redirect_uri": "http://redirect.uri",
            "scopes": "api read_user",
            "confidential": True,
        }
    )
    assert isinstance(application, CurrentUserApplication)
    assert application.id == 1
    assert application.secret == "secret"


def test_list_current_user_applications(current_user, resp_list_application):
    applications = current_user.applications.list()
    assert isinstance(applications[0], CurrentUserApplication)
    assert applications[0].application_name == "MyApplication"


def test_get_current_user_application(current_user, resp_get_application):
    application = current_user.applications.get(1)
    assert isinstance(application, CurrentUserApplication)
    assert application.callback_url == "http://redirect.uri"


def test_update_current_user_application(current_user, resp_update_application):
    application = current_user.applications.get(1)
    application.name = "UpdatedApplication"
    application.save()
    assert application.application_name == "UpdatedApplication"


def test_delete_current_user_application(current_user, resp_delete_application):
    current_user.applications.delete(1)

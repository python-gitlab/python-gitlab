import httpx
import pytest
import respx

import gitlab


@pytest.fixture
def gl_gql() -> gitlab.GraphQL:
    return gitlab.GraphQL("https://gitlab.example.com")


def test_import_error_includes_message(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gitlab.client, "_GQL_INSTALLED", False)
    with pytest.raises(ImportError, match="GraphQL client could not be initialized"):
        gitlab.GraphQL()


def test_graphql_as_context_manager_exits():
    with gitlab.GraphQL() as gl:
        assert isinstance(gl, gitlab.GraphQL)


def test_graphql_retries_on_429_response(
    gl_gql: gitlab.GraphQL, respx_mock: respx.MockRouter
):
    url = "https://gitlab.example.com/api/graphql"
    responses = [
        httpx.Response(429, headers={"retry-after": "1"}),
        httpx.Response(
            200, json={"data": {"currentUser": {"id": "gid://gitlab/User/1"}}}
        ),
    ]
    respx_mock.post(url).mock(side_effect=responses)
    gl_gql.execute("query {currentUser {id}}")


def test_graphql_raises_when_max_retries_exceeded(respx_mock: respx.MockRouter):
    url = "https://gitlab.example.com/api/graphql"
    responses = [
        httpx.Response(502),
        httpx.Response(502),
        httpx.Response(502),
    ]
    respx_mock.post(url).mock(side_effect=responses)

    gl_gql = gitlab.GraphQL(
        "https://gitlab.example.com", max_retries=1, retry_transient_errors=True
    )
    with pytest.raises(gitlab.GitlabHttpError):
        gl_gql.execute("query {currentUser {id}}")


def test_graphql_raises_on_401_response(
    gl_gql: gitlab.GraphQL, respx_mock: respx.MockRouter
):
    url = "https://gitlab.example.com/api/graphql"
    respx_mock.post(url).mock(return_value=httpx.Response(401))
    with pytest.raises(gitlab.GitlabAuthenticationError):
        gl_gql.execute("query {currentUser {id}}")

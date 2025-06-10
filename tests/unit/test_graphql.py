import httpx
import pytest
import respx

import gitlab


@pytest.fixture(scope="module")
def api_url() -> str:
    return "https://gitlab.example.com/api/graphql"


@pytest.fixture
def gl_gql() -> gitlab.GraphQL:
    return gitlab.GraphQL("https://gitlab.example.com")


@pytest.fixture
def gl_async_gql() -> gitlab.AsyncGraphQL:
    return gitlab.AsyncGraphQL("https://gitlab.example.com")


def test_import_error_includes_message(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gitlab.client, "_GQL_INSTALLED", False)
    with pytest.raises(ImportError, match="GraphQL client could not be initialized"):
        gitlab.GraphQL()


@pytest.mark.anyio
async def test_async_import_error_includes_message(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gitlab.client, "_GQL_INSTALLED", False)
    with pytest.raises(ImportError, match="GraphQL client could not be initialized"):
        gitlab.AsyncGraphQL()


def test_graphql_as_context_manager_exits():
    with gitlab.GraphQL() as gl:
        assert isinstance(gl, gitlab.GraphQL)


@pytest.mark.anyio
async def test_async_graphql_as_context_manager_aexits():
    async with gitlab.AsyncGraphQL() as gl:
        assert isinstance(gl, gitlab.AsyncGraphQL)


def test_graphql_retries_on_429_response(
    gl_gql: gitlab.GraphQL, respx_mock: respx.MockRouter
):
    """Test graphql_retries_on_429_response.

    query:

    query get_projects($first: Int = 2) {
        group(fullPath: "treeocean") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }

    reply:

    {
        "data": {
            "group": {
                "projects": {
                    "nodes": [
                        {
                            "id": "gid://gitlab/Project/491"
                        },
                        {
                            "id": "gid://gitlab/Project/485"
                        }
                    ]
                }
            }
        },
        "correlationId": "01JSJ7ERZ7N5PKA5RCBJQNG9CS"
    }
    """
    url = "https://gitlab.example.com/api/graphql"
    responses = [
        httpx.Response(429, headers={"retry-after": "1"}),
        httpx.Response(
            200,
            json={
                "data": {
                    "group": {
                        "projects": {
                            "nodes": [
                                {"id": "gid://gitlab/Project/491"},
                                {"id": "gid://gitlab/Project/485"},
                            ]
                        }
                    }
                },
                "correlationId": "01JSJ7ERZ7N5PKA5RCBJQNG9CS",
            },
        ),
    ]
    variable_values = {"first": 2}
    query = """
    query get_projects($first: Int) {
        group(fullPath: "python-gitlab") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }
    """
    respx_mock.post(url).mock(side_effect=responses)
    gl_gql.execute(query, variable_values=variable_values)


@pytest.mark.anyio
async def test_async_graphql_retries_on_429_response(
    api_url: str, gl_async_gql: gitlab.AsyncGraphQL, respx_mock: respx.MockRouter
):
    responses = [
        httpx.Response(429, headers={"retry-after": "1"}),
        httpx.Response(
            200, json={"data": {"currentUser": {"id": "gid://gitlab/User/1"}}}
        ),
    ]
    variable_values = {"first": 2}
    query = """
    query get_projects($first: Int) {
        group(fullPath: "python-gitlab") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }
    """

    respx_mock.post(api_url).mock(side_effect=responses)
    await gl_async_gql.execute(query, variable_values=variable_values)


def test_graphql_raises_when_max_retries_exceeded(
    api_url: str, respx_mock: respx.MockRouter
):
    responses = [httpx.Response(502), httpx.Response(502), httpx.Response(502)]
    respx_mock.post(api_url).mock(side_effect=responses)

    gl_gql = gitlab.GraphQL(
        "https://gitlab.example.com", max_retries=1, retry_transient_errors=True
    )
    variable_values = {"first": 2}
    query = """
    query get_projects($first: Int) {
        group(fullPath: "python-gitlab") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }
    """

    with pytest.raises(gitlab.GitlabHttpError):
        gl_gql.execute(query, variable_values=variable_values)


@pytest.mark.anyio
async def test_async_graphql_raises_when_max_retries_exceeded(
    api_url: str, respx_mock: respx.MockRouter
):
    responses = [httpx.Response(502), httpx.Response(502), httpx.Response(502)]
    respx_mock.post(api_url).mock(side_effect=responses)

    gl_async_gql = gitlab.AsyncGraphQL(
        "https://gitlab.example.com", max_retries=1, retry_transient_errors=True
    )
    variable_values = {"first": 2}
    query = """
    query get_projects($first: Int) {
        group(fullPath: "python-gitlab") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }
    """

    with pytest.raises(gitlab.GitlabHttpError):
        await gl_async_gql.execute(query, variable_values=variable_values)


def test_graphql_raises_on_401_response(
    api_url: str, gl_gql: gitlab.GraphQL, respx_mock: respx.MockRouter
):
    respx_mock.post(api_url).mock(return_value=httpx.Response(401))
    variable_values = {"first": 2}
    query = """
    query get_projects($first: Int) {
        group(fullPath: "python-gitlab") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }
    """

    with pytest.raises(gitlab.GitlabAuthenticationError):
        gl_gql.execute(query, variable_values=variable_values)


@pytest.mark.anyio
async def test_async_graphql_raises_on_401_response(
    api_url: str, gl_async_gql: gitlab.AsyncGraphQL, respx_mock: respx.MockRouter
):
    respx_mock.post(api_url).mock(return_value=httpx.Response(401))

    variable_values = {"first": 2}
    query = """
    query get_projects($first: Int) {
        group(fullPath: "python-gitlab") {
            projects(first: $first, includeSubgroups: true) {
                nodes {
                    id
                }
            }
        }
    }
    """

    with pytest.raises(gitlab.GitlabAuthenticationError):
        await gl_async_gql.execute(query, variable_values=variable_values)

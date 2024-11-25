import pytest

import gitlab


@pytest.fixture
def gl_gql(gitlab_url: str, gitlab_token: str) -> gitlab.GraphQL:
    return gitlab.GraphQL(gitlab_url, token=gitlab_token)


@pytest.fixture
def gl_async_gql(gitlab_url: str, gitlab_token: str) -> gitlab.AsyncGraphQL:
    return gitlab.AsyncGraphQL(gitlab_url, token=gitlab_token)


def test_query_returns_valid_response(gl_gql: gitlab.GraphQL):
    query = "query {currentUser {active}}"

    response = gl_gql.execute(query)
    assert response["currentUser"]["active"] is True


@pytest.mark.anyio
async def test_async_query_returns_valid_response(gl_async_gql: gitlab.AsyncGraphQL):
    query = "query {currentUser {active}}"

    response = await gl_async_gql.execute(query)
    assert response["currentUser"]["active"] is True

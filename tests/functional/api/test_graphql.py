import logging

import pytest

import gitlab


@pytest.fixture
def gl_gql(gitlab_url: str, gitlab_token: str) -> gitlab.GraphQL:
    logging.info("Instantiating gitlab.GraphQL instance")
    instance = gitlab.GraphQL(gitlab_url, token=gitlab_token)

    return instance


def test_query_returns_valid_response(gl_gql: gitlab.GraphQL):
    query = "query {currentUser {active}}"

    response = gl_gql.execute(query)
    assert response["currentUser"]["active"] is True

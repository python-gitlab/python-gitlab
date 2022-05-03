import pytest

import gitlab


@pytest.fixture(scope="session")
def graphql_gl(gitlab_service):
    url, private_token = gitlab_service
    return gitlab.GraphQLGitlab(url, oauth_token=private_token)

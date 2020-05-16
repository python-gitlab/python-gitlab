import pytest
import gitlab


@pytest.fixture
def gl():
    return gitlab.Gitlab(
        "http://localhost",
        private_token="private_token",
        ssl_verify=True,
        api_version=4,
    )

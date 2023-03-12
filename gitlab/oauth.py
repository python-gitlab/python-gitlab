import dataclasses
from typing import Optional


@dataclasses.dataclass
class PasswordCredentials:
    """
    Resource owner password credentials modelled according to
    https://docs.gitlab.com/ee/api/oauth2.html#resource-owner-password-credentials-flow
    https://datatracker.ietf.org/doc/html/rfc6749#section-4-3.

    If the GitLab server has disabled the ROPC flow without client credentials,
    client_id and client_secret must be provided.
    """

    username: str
    password: str
    grant_type: str = "password"
    scope: str = "api"
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    def __post_init__(self) -> None:
        basic_auth = (self.client_id, self.client_secret)

        if not any(basic_auth):
            self.basic_auth = None
            return

        if not all(basic_auth):
            raise TypeError("Both client_id and client_secret must be defined")

        self.basic_auth = basic_auth

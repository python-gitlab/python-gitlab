class GitlabError(Exception):
    def __init__(self, error_message="", response_code=None,
                 response_body=None):

        Exception.__init__(self, error_message)
        # Http status code
        self.response_code = response_code
        # Full http response
        self.response_body = response_body
        # Parsed error message from gitlab
        self.error_message = error_message

    def __str__(self):
        if self.response_code is not None:
            return "{0}: {1}".format(self.response_code, self.error_message)
        else:
            return "{0}".format(self.error_message)


class GitlabAuthenticationError(GitlabError):
    pass


class GitlabConnectionError(GitlabError):
    pass


class GitlabOperationError(GitlabError):
    pass


class GitlabListError(GitlabOperationError):
    pass


class GitlabGetError(GitlabOperationError):
    pass


class GitlabCreateError(GitlabOperationError):
    pass


class GitlabUpdateError(GitlabOperationError):
    pass


class GitlabDeleteError(GitlabOperationError):
    pass


class GitlabProtectError(GitlabOperationError):
    pass


class GitlabTransferProjectError(GitlabOperationError):
    pass


def raise_error_from_response(response, error, expected_code=200):
    """Tries to parse gitlab error message from response and raises error.

    Do nothing if the response status is the expected one.

    If response status code is 401, raises instead GitlabAuthenticationError.

    response: requests response object
    error: Error-class to raise. Should be inherited from GitLabError
    """

    if expected_code == response.status_code:
        return

    try:
        message = response.json()['message']
    except (KeyError, ValueError):
        message = response.content

    if response.status_code == 401:
        error = GitlabAuthenticationError

    raise error(error_message=message,
                response_code=response.status_code,
                response_body=response.content)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2015 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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


class GitlabBuildCancelError(GitlabOperationError):
    pass


class GitlabBuildRetryError(GitlabOperationError):
    pass


class GitlabBlockError(GitlabOperationError):
    pass


class GitlabUnblockError(GitlabOperationError):
    pass


class GitlabMRForbiddenError(GitlabOperationError):
    pass


class GitlabMRClosedError(GitlabOperationError):
    pass


class GitlabMROnBuildSuccessError(GitlabOperationError):
    pass


def raise_error_from_response(response, error, expected_code=200):
    """Tries to parse gitlab error message from response and raises error.

    Do nothing if the response status is the expected one.

    If response status code is 401, raises instead GitlabAuthenticationError.

    Args:
        response: requests response object
        error: Error-class or dict {return-code => class} of possible error
               class to raise. Should be inherited from GitLabError
    """

    if isinstance(expected_code, int):
        expected_codes = [expected_code]
    else:
        expected_codes = expected_code

    if response.status_code in expected_codes:
        return

    try:
        message = response.json()['message']
    except (KeyError, ValueError):
        message = response.content

    if isinstance(error, dict):
        error = error.get(response.status_code, GitlabOperationError)
    else:
        if response.status_code == 401:
            error = GitlabAuthenticationError

    raise error(error_message=message,
                response_code=response.status_code,
                response_body=response.content)

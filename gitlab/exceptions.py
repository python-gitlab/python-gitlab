from __future__ import annotations

import functools
from typing import Any, Callable, cast, TYPE_CHECKING, TypeVar


class GitlabError(Exception):
    def __init__(
        self,
        error_message: str | bytes = "",
        response_code: int | None = None,
        response_body: bytes | None = None,
    ) -> None:
        Exception.__init__(self, error_message)
        # Http status code
        self.response_code = response_code
        # Full http response
        self.response_body = response_body
        # Parsed error message from gitlab
        try:
            # if we receive str/bytes we try to convert to unicode/str to have
            # consistent message types (see #616)
            if TYPE_CHECKING:
                assert isinstance(error_message, bytes)
            self.error_message = error_message.decode()
        except Exception:
            if TYPE_CHECKING:
                assert isinstance(error_message, str)
            self.error_message = error_message

    def __str__(self) -> str:
        if self.response_code is not None:
            return f"{self.response_code}: {self.error_message}"
        return f"{self.error_message}"


class GitlabAuthenticationError(GitlabError):
    pass


class RedirectError(GitlabError):
    pass


class GitlabParsingError(GitlabError):
    pass


class GitlabCiLintError(GitlabError):
    pass


class GitlabConnectionError(GitlabError):
    pass


class GitlabOperationError(GitlabError):
    pass


class GitlabHttpError(GitlabError):
    pass


class GitlabListError(GitlabOperationError):
    pass


class GitlabGetError(GitlabOperationError):
    pass


class GitlabHeadError(GitlabOperationError):
    pass


class GitlabCreateError(GitlabOperationError):
    pass


class GitlabUpdateError(GitlabOperationError):
    pass


class GitlabDeleteError(GitlabOperationError):
    pass


class GitlabSetError(GitlabOperationError):
    pass


class GitlabProtectError(GitlabOperationError):
    pass


class GitlabTransferProjectError(GitlabOperationError):
    pass


class GitlabGroupTransferError(GitlabOperationError):
    pass


class GitlabProjectDeployKeyError(GitlabOperationError):
    pass


class GitlabPromoteError(GitlabOperationError):
    pass


class GitlabCancelError(GitlabOperationError):
    pass


class GitlabPipelineCancelError(GitlabCancelError):
    pass


class GitlabRetryError(GitlabOperationError):
    pass


class GitlabBuildCancelError(GitlabCancelError):
    pass


class GitlabBuildRetryError(GitlabRetryError):
    pass


class GitlabBuildPlayError(GitlabRetryError):
    pass


class GitlabBuildEraseError(GitlabRetryError):
    pass


class GitlabJobCancelError(GitlabCancelError):
    pass


class GitlabJobRetryError(GitlabRetryError):
    pass


class GitlabJobPlayError(GitlabRetryError):
    pass


class GitlabJobEraseError(GitlabRetryError):
    pass


class GitlabPipelinePlayError(GitlabRetryError):
    pass


class GitlabPipelineRetryError(GitlabRetryError):
    pass


class GitlabBlockError(GitlabOperationError):
    pass


class GitlabUnblockError(GitlabOperationError):
    pass


class GitlabDeactivateError(GitlabOperationError):
    pass


class GitlabActivateError(GitlabOperationError):
    pass


class GitlabBanError(GitlabOperationError):
    pass


class GitlabUnbanError(GitlabOperationError):
    pass


class GitlabSubscribeError(GitlabOperationError):
    pass


class GitlabUnsubscribeError(GitlabOperationError):
    pass


class GitlabMRForbiddenError(GitlabOperationError):
    pass


class GitlabMRApprovalError(GitlabOperationError):
    pass


class GitlabMRRebaseError(GitlabOperationError):
    pass


class GitlabMRResetApprovalError(GitlabOperationError):
    pass


class GitlabMRClosedError(GitlabOperationError):
    pass


class GitlabMROnBuildSuccessError(GitlabOperationError):
    pass


class GitlabTodoError(GitlabOperationError):
    pass


class GitlabTopicMergeError(GitlabOperationError):
    pass


class GitlabTimeTrackingError(GitlabOperationError):
    pass


class GitlabUploadError(GitlabOperationError):
    pass


class GitlabAttachFileError(GitlabOperationError):
    pass


class GitlabImportError(GitlabOperationError):
    pass


class GitlabInvitationError(GitlabOperationError):
    pass


class GitlabCherryPickError(GitlabOperationError):
    pass


class GitlabHousekeepingError(GitlabOperationError):
    pass


class GitlabOwnershipError(GitlabOperationError):
    pass


class GitlabSearchError(GitlabOperationError):
    pass


class GitlabStopError(GitlabOperationError):
    pass


class GitlabMarkdownError(GitlabOperationError):
    pass


class GitlabVerifyError(GitlabOperationError):
    pass


class GitlabRenderError(GitlabOperationError):
    pass


class GitlabRepairError(GitlabOperationError):
    pass


class GitlabRestoreError(GitlabOperationError):
    pass


class GitlabRevertError(GitlabOperationError):
    pass


class GitlabRotateError(GitlabOperationError):
    pass


class GitlabLicenseError(GitlabOperationError):
    pass


class GitlabFollowError(GitlabOperationError):
    pass


class GitlabUnfollowError(GitlabOperationError):
    pass


class GitlabUserApproveError(GitlabOperationError):
    pass


class GitlabUserRejectError(GitlabOperationError):
    pass


class GitlabDeploymentApprovalError(GitlabOperationError):
    pass


class GitlabHookTestError(GitlabOperationError):
    pass


# For an explanation of how these type-hints work see:
# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
#
# The goal here is that functions which get decorated will retain their types.
__F = TypeVar("__F", bound=Callable[..., Any])


def on_http_error(error: type[Exception]) -> Callable[[__F], __F]:
    """Manage GitlabHttpError exceptions.

    This decorator function can be used to catch GitlabHttpError exceptions
    raise specialized exceptions instead.

    Args:
        The exception type to raise -- must inherit from GitlabError
    """

    def wrap(f: __F) -> __F:
        @functools.wraps(f)
        def wrapped_f(*args: Any, **kwargs: Any) -> Any:
            try:
                return f(*args, **kwargs)
            except GitlabHttpError as e:
                raise error(e.error_message, e.response_code, e.response_body) from e

        return cast(__F, wrapped_f)

    return wrap


# Export manually to keep mypy happy
__all__ = [
    "GitlabActivateError",
    "GitlabAttachFileError",
    "GitlabAuthenticationError",
    "GitlabBanError",
    "GitlabBlockError",
    "GitlabBuildCancelError",
    "GitlabBuildEraseError",
    "GitlabBuildPlayError",
    "GitlabBuildRetryError",
    "GitlabCancelError",
    "GitlabCherryPickError",
    "GitlabCiLintError",
    "GitlabConnectionError",
    "GitlabCreateError",
    "GitlabDeactivateError",
    "GitlabDeleteError",
    "GitlabDeploymentApprovalError",
    "GitlabError",
    "GitlabFollowError",
    "GitlabGetError",
    "GitlabGroupTransferError",
    "GitlabHeadError",
    "GitlabHookTestError",
    "GitlabHousekeepingError",
    "GitlabHttpError",
    "GitlabImportError",
    "GitlabInvitationError",
    "GitlabJobCancelError",
    "GitlabJobEraseError",
    "GitlabJobPlayError",
    "GitlabJobRetryError",
    "GitlabLicenseError",
    "GitlabListError",
    "GitlabMRApprovalError",
    "GitlabMRClosedError",
    "GitlabMRForbiddenError",
    "GitlabMROnBuildSuccessError",
    "GitlabMRRebaseError",
    "GitlabMRResetApprovalError",
    "GitlabMarkdownError",
    "GitlabOperationError",
    "GitlabOwnershipError",
    "GitlabParsingError",
    "GitlabPipelineCancelError",
    "GitlabPipelinePlayError",
    "GitlabPipelineRetryError",
    "GitlabProjectDeployKeyError",
    "GitlabPromoteError",
    "GitlabProtectError",
    "GitlabRenderError",
    "GitlabRepairError",
    "GitlabRestoreError",
    "GitlabRetryError",
    "GitlabRevertError",
    "GitlabRotateError",
    "GitlabSearchError",
    "GitlabSetError",
    "GitlabStopError",
    "GitlabSubscribeError",
    "GitlabTimeTrackingError",
    "GitlabTodoError",
    "GitlabTopicMergeError",
    "GitlabTransferProjectError",
    "GitlabUnbanError",
    "GitlabUnblockError",
    "GitlabUnfollowError",
    "GitlabUnsubscribeError",
    "GitlabUpdateError",
    "GitlabUploadError",
    "GitlabUserApproveError",
    "GitlabUserRejectError",
    "GitlabVerifyError",
    "RedirectError",
]

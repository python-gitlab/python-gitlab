from gitlab import cli, utils
from gitlab import exceptions as exc
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin, UserAgentDetailMixin

from .award_emojis import ProjectSnippetAwardEmojiManager
from .discussions import ProjectSnippetDiscussionManager
from .notes import ProjectSnippetNoteManager, ProjectSnippetDiscussionNoteManager


__all__ = [
    "Snippet",
    "SnippetManager",
    "ProjectSnippet",
    "ProjectSnippetManager",
]


class Snippet(UserAgentDetailMixin, SaveMixin, ObjectDeleteMixin):
    _short_print_attr = "title"

    @cli.register_custom_action("Snippet")
    @exc.on_http_error(exc.GitlabGetError)
    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            str: The snippet content
        """
        path = "/snippets/%s/raw" % self.get_id()
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class SnippetManager(CRUDMixin):
    _path = "/snippets"
    _obj_cls = Snippet
    _create_attrs = (("title", "file_name", "content"), ("lifetime", "visibility"))
    _update_attrs = (tuple(), ("title", "file_name", "content", "visibility"))

    @cli.register_custom_action("SnippetManager")
    def public(self, **kwargs):
        """List all the public snippets.

        Args:
            all (bool): If True the returned object will be a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: A generator for the snippets list
        """
        return self.list(path="/snippets/public", **kwargs)


class ProjectSnippet(UserAgentDetailMixin, SaveMixin, ObjectDeleteMixin):
    _url = "/projects/%(project_id)s/snippets"
    _short_print_attr = "title"
    _managers = (
        ("awardemojis", "ProjectSnippetAwardEmojiManager"),
        ("discussions", "ProjectSnippetDiscussionManager"),
        ("notes", "ProjectSnippetNoteManager"),
    )

    @cli.register_custom_action("ProjectSnippet")
    @exc.on_http_error(exc.GitlabGetError)
    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            str: The snippet content
        """
        path = "%s/%s/raw" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectSnippetManager(CRUDMixin):
    _path = "/projects/%(project_id)s/snippets"
    _obj_cls = ProjectSnippet
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("title", "file_name", "content", "visibility"), ("description",))
    _update_attrs = (
        tuple(),
        ("title", "file_name", "content", "visibility", "description"),
    )

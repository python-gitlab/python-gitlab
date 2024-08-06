import pytest

import gitlab


def test_snippets(gl):
    snippets = gl.snippets.list(get_all=True)
    assert not snippets

    snippet = gl.snippets.create(
        {
            "title": "snippet1",
            "files": [{"file_path": "snippet1.py", "content": "import gitlab"}],
        }
    )
    snippet = gl.snippets.get(snippet.id)
    snippet.title = "updated_title"
    snippet.save()

    snippet = gl.snippets.get(snippet.id)
    assert snippet.title == "updated_title"

    content = snippet.content()
    assert content.decode() == "import gitlab"

    all_snippets = gl.snippets.list_all(get_all=True)
    public_snippets = gl.snippets.public(get_all=True)
    list_public_snippets = gl.snippets.list_public(get_all=True)
    assert isinstance(all_snippets, list)
    assert isinstance(list_public_snippets, list)
    assert public_snippets == list_public_snippets

    snippet.delete()


def test_project_snippets(project):
    project.snippets_enabled = True
    project.save()

    snippet = project.snippets.create(
        {
            "title": "snip1",
            "files": [{"file_path": "foo.py", "content": "initial content"}],
            "visibility": gitlab.const.VISIBILITY_PRIVATE,
        }
    )

    assert snippet.title == "snip1"


@pytest.mark.xfail(reason="Returning 404 UserAgentDetail not found in GL 16")
def test_project_snippet_user_agent_detail(project):
    snippet = project.snippets.list()[0]

    user_agent_detail = snippet.user_agent_detail()

    assert user_agent_detail["user_agent"]


def test_project_snippet_discussion(project):
    snippet = project.snippets.list()[0]

    discussion = snippet.discussions.create({"body": "Discussion body"})
    assert discussion in snippet.discussions.list()

    note = discussion.notes.create({"body": "first note"})
    note_from_get = discussion.notes.get(note.id)
    note_from_get.body = "updated body"
    note_from_get.save()

    discussion = snippet.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"

    note_from_get.delete()


def test_project_snippet_file(project):
    snippet = project.snippets.list()[0]
    snippet.file_name = "bar.py"
    snippet.save()

    snippet = project.snippets.get(snippet.id)
    assert snippet.content().decode() == "initial content"
    assert snippet.file_name == "bar.py"
    assert snippet in project.snippets.list()

    snippet.delete()

import gitlab


def test_snippets(gl):
    snippets = gl.snippets.list(all=True)
    assert len(snippets) == 0

    snippet = gl.snippets.create(
        {"title": "snippet1", "file_name": "snippet1.py", "content": "import gitlab"}
    )
    snippet = gl.snippets.get(snippet.id)
    snippet.title = "updated_title"
    snippet.save()

    snippet = gl.snippets.get(snippet.id)
    assert snippet.title == "updated_title"

    content = snippet.content()
    assert content.decode() == "import gitlab"
    assert snippet.user_agent_detail()["user_agent"]

    snippet.delete()
    snippets = gl.snippets.list(all=True)
    assert len(snippets) == 0


def test_project_snippets(project):
    project.snippets_enabled = True
    project.save()

    snippet = project.snippets.create(
        {
            "title": "snip1",
            "file_name": "foo.py",
            "content": "initial content",
            "visibility": gitlab.const.VISIBILITY_PRIVATE,
        }
    )

    assert snippet.user_agent_detail()["user_agent"]


def test_project_snippet_discussion(project):
    snippet = project.snippets.list()[0]
    size = len(snippet.discussions.list())

    discussion = snippet.discussions.create({"body": "Discussion body"})
    assert len(snippet.discussions.list()) == size + 1

    note = discussion.notes.create({"body": "first note"})
    note_from_get = discussion.notes.get(note.id)
    note_from_get.body = "updated body"
    note_from_get.save()

    discussion = snippet.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"

    note_from_get.delete()
    discussion = snippet.discussions.get(discussion.id)
    assert len(discussion.attributes["notes"]) == 1


def test_project_snippet_file(project):
    snippet = project.snippets.list()[0]
    snippet.file_name = "bar.py"
    snippet.save()

    snippet = project.snippets.get(snippet.id)
    assert snippet.content().decode() == "initial content"
    assert snippet.file_name == "bar.py"

    size = len(project.snippets.list())
    snippet.delete()
    assert len(project.snippets.list()) == (size - 1)

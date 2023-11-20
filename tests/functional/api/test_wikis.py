"""
GitLab API:
https://docs.gitlab.com/ee/api/wikis.html
"""


def test_project_wikis(project):
    page = project.wikis.create({"title": "title/subtitle", "content": "test content"})
    page.content = "update content"
    page.title = "subtitle"

    page.save()

    page.delete()


def test_project_wiki_file_upload(project):
    page = project.wikis.create(
        {"title": "title/subtitle", "content": "test page content"}
    )
    filename = "test.txt"
    file_contents = "testing contents"

    uploaded_file = page.upload(filename, file_contents)

    link = uploaded_file["link"]
    file_name = uploaded_file["file_name"]
    file_path = uploaded_file["file_path"]
    assert file_name == filename
    assert file_path.startswith("uploads/")
    assert file_path.endswith(f"/{filename}")
    assert link["url"] == file_path
    assert link["markdown"] == f"[{file_name}]({file_path})"


def test_group_wikis(group):
    page = group.wikis.create({"title": "title/subtitle", "content": "test content"})
    page.content = "update content"
    page.title = "subtitle"

    page.save()

    page.delete()


def test_group_wiki_file_upload(group):
    page = group.wikis.create(
        {"title": "title/subtitle", "content": "test page content"}
    )
    filename = "test.txt"
    file_contents = "testing contents"

    uploaded_file = page.upload(filename, file_contents)

    link = uploaded_file["link"]
    file_name = uploaded_file["file_name"]
    file_path = uploaded_file["file_path"]
    assert file_name == filename
    assert file_path.startswith("uploads/")
    assert file_path.endswith(f"/{filename}")
    assert link["url"] == file_path
    assert link["markdown"] == f"[{file_name}]({file_path})"

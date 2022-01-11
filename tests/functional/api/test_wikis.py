"""
GitLab API:
https://docs.gitlab.com/ee/api/wikis.html
"""


def test_wikis(project):
    page = project.wikis.create({"title": "title/subtitle", "content": "test content"})
    page.content = "update content"
    page.title = "subtitle"

    page.save()

    page.delete()

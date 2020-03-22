from httmock import urlmatch, response, with_httmock

from .test_projects import headers, TestProject


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/repository/commits/6b2257ea",
    method="get",
)
def resp_get_commit(url, request):
    """Mock for commit GET response."""
    content = """{
    "id": "6b2257eabcec3db1f59dafbd84935e3caea04235",
    "short_id": "6b2257ea",
    "title": "Initial commit"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", path="/api/v4/projects/1/repository/commits", method="post",
)
def resp_create_commit(url, request):
    """Mock for commit create POST response."""
    content = """{
    "id": "ed899a2f4b50b4370feeea94676502b42383c746",
    "short_id": "ed899a2f",
    "title": "Commit message"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", path="/api/v4/projects/1/repository/commits/6b2257ea", method="post",
)
def resp_revert_commit(url, request):
    """Mock for commit revert POST response."""
    content = """{
    "id": "8b090c1b79a14f2bd9e8a738f717824ff53aebad",
    "short_id": "8b090c1b",
    "title":"Revert \\"Initial commit\\""
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


class TestCommit(TestProject):
    """
    Base class for commit tests. Inherits from TestProject,
    since currently all commit methods are under projects.
    """

    @with_httmock(resp_get_commit)
    def test_get_commit(self):
        commit = self.project.commits.get("6b2257ea")
        self.assertEqual(commit.short_id, "6b2257ea")
        self.assertEqual(commit.title, "Initial commit")

    @with_httmock(resp_create_commit)
    def test_create_commit(self):
        data = {
            "branch": "master",
            "commit_message": "Commit message",
            "actions": [{"action": "create", "file_path": "README", "content": "",}],
        }
        commit = self.project.commits.create(data)
        self.assertEqual(commit.short_id, "ed899a2f")
        self.assertEqual(commit.title, data["commit_message"])

    @with_httmock(resp_revert_commit)
    def test_revert_commit(self):
        commit = self.project.commits.get("6b2257ea", lazy=True)
        revert_commit = commit.revert(branch="master")
        self.assertEqual(revert_commit["short_id"], "8b090c1b")
        self.assertEqual(revert_commit["title"], 'Revert "Initial commit"')

import pytest

import gitlab


def test_import_error_includes_message(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(gitlab.client, "_GQL_INSTALLED", False)
    with pytest.raises(ImportError, match="GraphQL client could not be initialized"):
        gitlab.GraphQL()


def test_graphql_as_context_manager_exits():
    with gitlab.GraphQL() as gl:
        assert isinstance(gl, gitlab.GraphQL)

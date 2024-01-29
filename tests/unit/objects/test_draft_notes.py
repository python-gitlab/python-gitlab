"""
GitLab API: https://docs.gitlab.com/ee/api/draft_notes.html
"""

from copy import deepcopy

import pytest
import responses

from gitlab.v4.objects import ProjectMergeRequestDraftNote

draft_note_content = {
    "id": 1,
    "author_id": 23,
    "merge_request_id": 1,
    "resolve_discussion": False,
    "discussion_id": None,
    "note": "Example title",
    "commit_id": None,
    "line_code": None,
    "position": {
        "base_sha": None,
        "start_sha": None,
        "head_sha": None,
        "old_path": None,
        "new_path": None,
        "position_type": "text",
        "old_line": None,
        "new_line": None,
        "line_range": None,
    },
}


@pytest.fixture()
def resp_list_merge_request_draft_notes():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes",
            json=[draft_note_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_get_merge_request_draft_note():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes/1",
            json=draft_note_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_create_merge_request_draft_note():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes",
            json=draft_note_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture()
def resp_update_merge_request_draft_note():
    updated_content = deepcopy(draft_note_content)
    updated_content["note"] = "New title"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes/1",
            json=updated_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture()
def resp_delete_merge_request_draft_note():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes/1",
            json=draft_note_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture()
def resp_publish_merge_request_draft_note():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes/1/publish",
            status=204,
        )
        yield rsps


@pytest.fixture()
def resp_bulk_publish_merge_request_draft_notes():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/merge_requests/1/draft_notes/bulk_publish",
            status=204,
        )
        yield rsps


def test_list_merge_requests_draft_notes(
    project_merge_request, resp_list_merge_request_draft_notes
):
    draft_notes = project_merge_request.draft_notes.list()
    assert len(draft_notes) == 1
    assert isinstance(draft_notes[0], ProjectMergeRequestDraftNote)
    assert draft_notes[0].note == draft_note_content["note"]


def test_get_merge_requests_draft_note(
    project_merge_request, resp_get_merge_request_draft_note
):
    draft_note = project_merge_request.draft_notes.get(1)
    assert isinstance(draft_note, ProjectMergeRequestDraftNote)
    assert draft_note.note == draft_note_content["note"]


def test_create_merge_requests_draft_note(
    project_merge_request, resp_create_merge_request_draft_note
):
    draft_note = project_merge_request.draft_notes.create({"note": "Example title"})
    assert isinstance(draft_note, ProjectMergeRequestDraftNote)
    assert draft_note.note == draft_note_content["note"]


def test_update_merge_requests_draft_note(
    project_merge_request, resp_update_merge_request_draft_note
):
    draft_note = project_merge_request.draft_notes.get(1, lazy=True)
    draft_note.note = "New title"
    draft_note.save()
    assert draft_note.note == "New title"


def test_delete_merge_requests_draft_note(
    project_merge_request, resp_delete_merge_request_draft_note
):
    draft_note = project_merge_request.draft_notes.get(1, lazy=True)
    draft_note.delete()


def test_publish_merge_requests_draft_note(
    project_merge_request, resp_publish_merge_request_draft_note
):
    draft_note = project_merge_request.draft_notes.get(1, lazy=True)
    draft_note.publish()


def test_bulk_publish_merge_requests_draft_notes(
    project_merge_request, resp_bulk_publish_merge_request_draft_notes
):
    project_merge_request.draft_notes.bulk_publish()

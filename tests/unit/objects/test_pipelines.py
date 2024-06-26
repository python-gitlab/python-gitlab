"""
GitLab API: https://docs.gitlab.com/ee/api/pipelines.html
"""

import pytest
import responses

from gitlab.v4.objects import (
    ProjectPipeline,
    ProjectPipelineTestReport,
    ProjectPipelineTestReportSummary,
)

pipeline_content = {
    "id": 46,
    "project_id": 1,
    "status": "pending",
    "ref": "main",
    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "tag": False,
    "yaml_errors": None,
    "user": {
        "name": "Administrator",
        "username": "root",
        "id": 1,
        "state": "active",
        "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "http://localhost:3000/root",
    },
    "created_at": "2016-08-11T11:28:34.085Z",
    "updated_at": "2016-08-11T11:32:35.169Z",
    "started_at": None,
    "finished_at": "2016-08-11T11:32:35.145Z",
    "committed_at": None,
    "duration": None,
    "queued_duration": 0.010,
    "coverage": None,
    "web_url": "https://example.com/foo/bar/pipelines/46",
}

pipeline_latest = {
    "id": 47,
    "project_id": 1,
    "status": "pending",
    "ref": "main",
    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "tag": False,
    "yaml_errors": None,
    "user": {
        "name": "Administrator",
        "username": "root",
        "id": 1,
        "state": "active",
        "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "http://localhost:3000/root",
    },
    "created_at": "2016-08-11T11:28:34.085Z",
    "updated_at": "2016-08-11T11:32:35.169Z",
    "started_at": None,
    "finished_at": "2016-08-11T11:32:35.145Z",
    "committed_at": None,
    "duration": None,
    "queued_duration": 0.010,
    "coverage": None,
    "web_url": "https://example.com/foo/bar/pipelines/46",
}

pipeline_latest_other_ref = {
    "id": 48,
    "project_id": 1,
    "status": "pending",
    "ref": "feature-ref",
    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "tag": False,
    "yaml_errors": None,
    "user": {
        "name": "Administrator",
        "username": "root",
        "id": 1,
        "state": "active",
        "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "http://localhost:3000/root",
    },
    "created_at": "2016-08-11T11:28:34.085Z",
    "updated_at": "2016-08-11T11:32:35.169Z",
    "started_at": None,
    "finished_at": "2016-08-11T11:32:35.145Z",
    "committed_at": None,
    "duration": None,
    "queued_duration": 0.010,
    "coverage": None,
    "web_url": "https://example.com/foo/bar/pipelines/46",
}


test_report_content = {
    "total_time": 5,
    "total_count": 1,
    "success_count": 1,
    "failed_count": 0,
    "skipped_count": 0,
    "error_count": 0,
    "test_suites": [
        {
            "name": "Secure",
            "total_time": 5,
            "total_count": 1,
            "success_count": 1,
            "failed_count": 0,
            "skipped_count": 0,
            "error_count": 0,
            "test_cases": [
                {
                    "status": "success",
                    "name": "Security Reports can create an auto-remediation MR",
                    "classname": "vulnerability_management_spec",
                    "execution_time": 5,
                    "system_output": None,
                    "stack_trace": None,
                }
            ],
        }
    ],
}


test_report_summary_content = {
    "total": {
        "time": 1904,
        "count": 3363,
        "success": 3351,
        "failed": 0,
        "skipped": 12,
        "error": 0,
        "suite_error": None,
    },
    "test_suites": [
        {
            "name": "test",
            "total_time": 1904,
            "total_count": 3363,
            "success_count": 3351,
            "failed_count": 0,
            "skipped_count": 12,
            "error_count": 0,
            "build_ids": [66004],
            "suite_error": None,
        }
    ],
}


@pytest.fixture
def resp_get_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/1",
            json=pipeline_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_cancel_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipelines/1/cancel",
            json=pipeline_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_retry_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipelines/1/retry",
            json=pipeline_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_get_pipeline_test_report():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/1/test_report",
            json=test_report_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_pipeline_test_report_summary():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/1/test_report_summary",
            json=test_report_summary_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_latest():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/latest",
            json=pipeline_latest,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_latest_other_ref():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/latest",
            json=pipeline_latest_other_ref,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_get_project_pipeline(project, resp_get_pipeline):
    pipeline = project.pipelines.get(1)
    assert isinstance(pipeline, ProjectPipeline)
    assert pipeline.ref == "main"
    assert pipeline.id == 46


def test_cancel_project_pipeline(project, resp_cancel_pipeline):
    pipeline = project.pipelines.get(1, lazy=True)

    output = pipeline.cancel()
    assert output["ref"] == "main"


def test_retry_project_pipeline(project, resp_retry_pipeline):
    pipeline = project.pipelines.get(1, lazy=True)

    output = pipeline.retry()
    assert output["ref"] == "main"


def test_get_project_pipeline_test_report(project, resp_get_pipeline_test_report):
    pipeline = project.pipelines.get(1, lazy=True)
    test_report = pipeline.test_report.get()
    assert isinstance(test_report, ProjectPipelineTestReport)
    assert test_report.total_time == 5
    assert test_report.test_suites[0]["name"] == "Secure"


def test_get_project_pipeline_test_report_summary(
    project, resp_get_pipeline_test_report_summary
):
    pipeline = project.pipelines.get(1, lazy=True)
    test_report_summary = pipeline.test_report_summary.get()
    assert isinstance(test_report_summary, ProjectPipelineTestReportSummary)
    assert test_report_summary.total["count"] == 3363
    assert test_report_summary.test_suites[0]["name"] == "test"


def test_latest_pipeline(project, resp_get_latest):
    pipeline = project.pipelines.latest()
    assert isinstance(pipeline, ProjectPipeline)
    assert pipeline.ref == "main"
    assert pipeline.id == 47


def test_latest_pipeline_other_ref(project, resp_get_latest_other_ref):
    pipeline = project.pipelines.latest(ref="feature-ref")
    assert isinstance(pipeline, ProjectPipeline)
    assert pipeline.ref == "feature-ref"
    assert pipeline.id == 48

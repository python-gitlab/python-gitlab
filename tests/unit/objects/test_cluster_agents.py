"""
GitLab API: https://docs.gitlab.com/ee/api/cluster_agents.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectClusterAgent

agent_content = {
    "id": 1,
    "name": "agent-1",
    "config_project": {
        "id": 20,
        "description": "",
        "name": "test",
        "name_with_namespace": "Administrator / test",
        "path": "test",
        "path_with_namespace": "root/test",
        "created_at": "2022-03-20T20:42:40.221Z",
    },
    "created_at": "2022-04-20T20:42:40.221Z",
    "created_by_user_id": 42,
}


@pytest.fixture
def resp_list_project_cluster_agents():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/cluster_agents",
            json=[agent_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_project_cluster_agent():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/cluster_agents/1",
            json=agent_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_project_cluster_agent():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/cluster_agents",
            json=agent_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_project_cluster_agent():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/cluster_agents/1",
            status=204,
        )
        yield rsps


def test_list_project_cluster_agents(project, resp_list_project_cluster_agents):
    agent = project.cluster_agents.list()[0]
    assert isinstance(agent, ProjectClusterAgent)
    assert agent.name == "agent-1"


def test_get_project_cluster_agent(project, resp_get_project_cluster_agent):
    agent = project.cluster_agents.get(1)
    assert isinstance(agent, ProjectClusterAgent)
    assert agent.name == "agent-1"


def test_create_project_cluster_agent(project, resp_create_project_cluster_agent):
    agent = project.cluster_agents.create({"name": "agent-1"})
    assert isinstance(agent, ProjectClusterAgent)
    assert agent.name == "agent-1"


def test_delete_project_cluster_agent(project, resp_delete_project_cluster_agent):
    agent = project.cluster_agents.get(1, lazy=True)
    agent.delete()

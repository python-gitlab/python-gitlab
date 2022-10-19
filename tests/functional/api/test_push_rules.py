import pytest

import gitlab


@pytest.mark.gitlab_premium
def test_project_push_rules(project):
    with pytest.raises(gitlab.GitlabParsingError):
        # when no rules are defined the API call returns back `None` which
        # causes a gitlab.GitlabParsingError in RESTObject.__init__()
        project.pushrules.get()

    push_rules = project.pushrules.create({"deny_delete_tag": True})
    assert push_rules.deny_delete_tag

    push_rules.deny_delete_tag = False
    push_rules.save()

    push_rules = project.pushrules.get()
    assert push_rules
    assert not push_rules.deny_delete_tag

    push_rules.delete()

    with pytest.raises(gitlab.GitlabParsingError):
        project.pushrules.get()

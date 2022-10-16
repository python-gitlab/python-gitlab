import pytest


@pytest.mark.xfail(reason="need to relax RESTObject init for non-dict responses")
def test_project_push_rules(project):
    push_rules = project.pushrules.get()
    assert not push_rules

    push_rules = project.pushrules.create({"deny_delete_tag": True})
    assert push_rules.deny_delete_tag

    push_rules.deny_delete_tag = False
    push_rules.save()

    push_rules = project.pushrules.get()
    assert push_rules
    assert not push_rules.deny_delete_tag

    push_rules.delete()
    assert not push_rules

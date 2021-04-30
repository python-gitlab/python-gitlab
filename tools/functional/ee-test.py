#!/usr/bin/env python

import gitlab


P1 = "root/project1"
P2 = "root/project2"
MR_P1 = 1
I_P1 = 1
I_P2 = 1
EPIC_ISSUES = [4, 5]
G1 = "group1"
LDAP_CN = "app1"
LDAP_PROVIDER = "ldapmain"


def start_log(message):
    print("Testing %s... " % message, end="")


def end_log():
    print("OK")


gl = gitlab.Gitlab.from_config("ee")
project1 = gl.projects.get(P1)
project2 = gl.projects.get(P2)
issue_p1 = project1.issues.get(I_P1)
issue_p2 = project2.issues.get(I_P2)
group1 = gl.groups.get(G1)
mr = project1.mergerequests.get(1)

start_log("MR approvals")
approval = project1.approvals.get()
v = approval.reset_approvals_on_push
approval.reset_approvals_on_push = not v
approval.save()
approval = project1.approvals.get()
assert v != approval.reset_approvals_on_push
project1.approvals.set_approvers(1, [1], [])
approval = project1.approvals.get()
assert approval.approvers[0]["user"]["id"] == 1

approval = mr.approvals.get()
approval.approvals_required = 2
approval.save()
approval = mr.approvals.get()
assert approval.approvals_required == 2
approval.approvals_required = 3
approval.save()
approval = mr.approvals.get()
assert approval.approvals_required == 3
mr.approvals.set_approvers(1, [1], [])
approval = mr.approvals.get()
assert approval.approvers[0]["user"]["id"] == 1

ars = project1.approvalrules.list(all=True)
assert len(ars) == 0
project1.approvalrules.create(
    {"name": "approval-rule", "approvals_required": 1, "group_ids": [group1.id]}
)
ars = project1.approvalrules.list(all=True)
assert len(ars) == 1
assert ars[0].approvals_required == 2
ars[0].save()
ars = project1.approvalrules.list(all=True)
assert len(ars) == 1
assert ars[0].approvals_required == 2
ars[0].delete()
ars = project1.approvalrules.list(all=True)
assert len(ars) == 0
end_log()

start_log("geo nodes")
# very basic tests because we only have 1 node...
nodes = gl.geonodes.list()
status = gl.geonodes.status()
end_log()

start_log("issue links")
# bit of cleanup just in case
for link in issue_p1.links.list():
    issue_p1.links.delete(link.issue_link_id)

src, dst = issue_p1.links.create({"target_project_id": P2, "target_issue_iid": I_P2})
links = issue_p1.links.list()
link_id = links[0].issue_link_id
issue_p1.links.delete(link_id)
end_log()

start_log("LDAP links")
# bit of cleanup just in case
if hasattr(group1, "ldap_group_links"):
    for link in group1.ldap_group_links:
        group1.delete_ldap_group_link(link["cn"], link["provider"])
assert gl.ldapgroups.list()
group1.add_ldap_group_link(LDAP_CN, 30, LDAP_PROVIDER)
group1.ldap_sync()
group1.delete_ldap_group_link(LDAP_CN)
end_log()

start_log("boards")
# bit of cleanup just in case
for board in project1.boards.list():
    if board.name == "testboard":
        board.delete()
board = project1.boards.create({"name": "testboard"})
board = project1.boards.get(board.id)
project1.boards.delete(board.id)

for board in group1.boards.list():
    if board.name == "testboard":
        board.delete()
board = group1.boards.create({"name": "testboard"})
board = group1.boards.get(board.id)
group1.boards.delete(board.id)
end_log()

start_log("push rules")
pr = project1.pushrules.get()
if pr:
    pr.delete()
pr = project1.pushrules.create({"deny_delete_tag": True})
pr.deny_delete_tag = False
pr.save()
pr = project1.pushrules.get()
assert pr is not None
assert pr.deny_delete_tag is False
pr.delete()
end_log()

start_log("license")
license = gl.get_license()
assert "user_limit" in license
try:
    gl.set_license("dummykey")
except Exception as e:
    assert "The license key is invalid." in e.error_message
end_log()

start_log("epics")
epic = group1.epics.create({"title": "Test epic"})
epic.title = "Fixed title"
epic.labels = ["label1", "label2"]
epic.save()
epic = group1.epics.get(epic.iid)
assert epic.title == "Fixed title"
assert len(group1.epics.list())

# issues
assert not epic.issues.list()
for i in EPIC_ISSUES:
    epic.issues.create({"issue_id": i})
assert len(EPIC_ISSUES) == len(epic.issues.list())
for ei in epic.issues.list():
    ei.delete()

epic.delete()
end_log()

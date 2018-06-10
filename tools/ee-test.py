#!/usr/bin/env python

import gitlab


P1 = 'root/project1'
P2 = 'root/project2'
I_P1 = 1
I_P2 = 1
G1 = 'group1'
LDAP_CN = 'app1'
LDAP_PROVIDER = 'ldapmain'


def start_log(message):
    print('Testing %s... ' % message, end='')


def end_log():
    print('OK')


gl = gitlab.Gitlab.from_config('ee')
project1 = gl.projects.get(P1)
project2 = gl.projects.get(P2)
issue_p1 = project1.issues.get(I_P1)
issue_p2 = project2.issues.get(I_P2)
group1 = gl.groups.get(G1)

start_log('MR approvals')
approval = project1.approvals.get()
v = approval.reset_approvals_on_push
approval.reset_approvals_on_push = not v
approval.save()
approval = project1.approvals.get()
assert(v != approval.reset_approvals_on_push)
project1.approvals.set_approvers([1], [])
approval = project1.approvals.get()
assert(approval.approvers[0]['user']['id'] == 1)
end_log()

start_log('geo nodes')
# very basic tests because we only have 1 node...
nodes = gl.geonodes.list()
status = gl.geonodes.status()
end_log()

start_log('issue links')
# bit of cleanup just in case
for link in issue_p1.links.list():
    issue_p1.links.delete(link.issue_link_id)

src, dst = issue_p1.links.create({'target_project_id': P2,
                                  'target_issue_iid': I_P2})
links = issue_p1.links.list()
link_id = links[0].issue_link_id
issue_p1.links.delete(link_id)
end_log()

start_log('LDAP links')
# bit of cleanup just in case
if hasattr(group1, 'ldap_group_links'):
    for link in group1.ldap_group_links:
        group1.delete_ldap_group_link(link['cn'], link['provider'])
group1.add_ldap_group_link(LDAP_CN, 30, LDAP_PROVIDER)
group1.ldap_sync()
group1.delete_ldap_group_link(LDAP_CN)
end_log()

start_log('Boards')
# bit of cleanup just in case
for board in project1.boards.list():
    if board.name == 'testboard':
        board.delete()
board = project1.boards.create({'name': 'testboard'})
board = project1.boards.get(board.id)
project1.boards.delete(board.id)

for board in group1.boards.list():
    if board.name == 'testboard':
        board.delete()
board = group1.boards.create({'name': 'testboard'})
board = group1.boards.get(board.id)
group1.boards.delete(board.id)
end_log()

#!/usr/bin/env python

import gitlab


P1 = 'root/project1'
P2 = 'root/project2'
I_P1 = 1
I_P2 = 1


def start_log(message):
    print('Testing %s... ' % message, end='')


def end_log():
    print('OK')


gl = gitlab.Gitlab.from_config('ee')
project1 = gl.projects.get(P1)
project2 = gl.projects.get(P2)
issue_p1 = project1.issues.get(I_P1)
issue_p2 = project2.issues.get(I_P2)

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

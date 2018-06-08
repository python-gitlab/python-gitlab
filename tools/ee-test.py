#!/usr/bin/env python

import gitlab


PROJECT_NAME = 'root/project1'

def start_log(message):
    print('Testing %s... ' % message, end='')


def end_log():
    print('OK')


gl = gitlab.Gitlab.from_config('ee')
project = gl.projects.get(PROJECT_NAME)

start_log('MR approvals')
approval = project.approvals.get()
v = approval.reset_approvals_on_push
approval.reset_approvals_on_push = not v
approval.save()
approval = project.approvals.get()
assert(v != approval.reset_approvals_on_push)
project.approvals.set_approvers([1], [])
approval = project.approvals.get()
assert(approval.approvers[0]['user']['id'] == 1)
end_log()

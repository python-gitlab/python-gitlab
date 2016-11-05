# list
mrs = gl.project_mergerequests.list(project_id=1)
# or
mrs = project.mergerequests.list()
# end list

# filtered list
mrs = project.mergerequests.list(state='merged', order_by='updated_at')
# end filtered list

# get
mr = gl.project_mergerequests.get(mr_id, project_id=1)
# or
mr = project.mergerequests.get(mr_id)
# end get

# create
mr = gl.project_mergerequests.create({'source_branch': 'cool_feature',
                                      'target_branch': 'master',
                                      'title': 'merge cool feature'},
                                     project_id=1)
# or
mr = project.mergerequests.create({'source_branch': 'cool_feature',
                                   'target_branch': 'master',
                                   'title': 'merge cool feature'})
# end create

# update
mr.description = 'New description'
mr.save()
# end update

# state
mr.state_event = 'close'  # or 'reopen'
mr.save()
# end state

# delete
gl.project_mergerequests.delete(mr_id, project_id=1)
# or
project.mergerequests.delete(mr_id)
# or
mr.delete()
# end delete

# merge
mr.merge()
# end merge

# cancel
mr.cancel_merge_when_build_succeeds()
# end cancel

# issues
mr.closes_issues()
# end issues

# subscribe
mr.subscribe()
mr.unsubscribe()
# end subscribe

# todo
mr.todo()
# end todo

# diff list
diffs = mr.diffs.list()
# end diff list

# diff get
diff = mr.diffs.get(diff_id)
# end diff get

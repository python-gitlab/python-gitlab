# var list
variables = project.variables.list()
# end var list

# var get
var = project.variables.get(var_key)
# end var get

# var create
var = project.variables.create({'key': 'key1', 'value': 'value1'})
# end var create

# var update
var.value = 'new_value'
var.save()
# end var update

# var delete
project.variables.delete(var_key)
# or
var.delete()
# end var delete

# trigger list
triggers = project.triggers.list()
# end trigger list

# trigger get
trigger = project.triggers.get(trigger_token)
# end trigger get

# trigger create
trigger = project.triggers.create({})
# end trigger create

# trigger delete
project.triggers.delete(trigger_token)
# or
trigger.delete()
# end trigger delete

# list
builds = project.builds.list()  # v3
jobs = project.jobs.list()  # v4
# end list

# commit list
# v3 only
commit = gl.project_commits.get(commit_sha, project_id=1)
builds = commit.builds()
# end commit list

# get
project.builds.get(build_id)  # v3
project.jobs.get(job_id)  # v4
# end get

# artifacts
build_or_job.artifacts()
# end artifacts

# stream artifacts
class Foo(object):
    def __init__(self):
        self._fd = open('artifacts.zip', 'wb')

    def __call__(self, chunk):
        self._fd.write(chunk)

target = Foo()
build_or_job.artifacts(streamed=True, action=target)
del(target)  # flushes data on disk
# end stream artifacts

# keep artifacts
build_or_job.keep_artifacts()
# end keep artifacts

# trace
build_or_job.trace()
# end trace

# retry
build_or_job.cancel()
build_or_job.retry()
# end retry

# erase
build_or_job.erase()
# end erase

# play
build_or_job.play()
# end play

# trigger run
project.trigger_build('master', trigger_token,
                      {'extra_var1': 'foo', 'extra_var2': 'bar'})
# end trigger run

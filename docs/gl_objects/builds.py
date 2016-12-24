# var list
variables = gl.project_variables.list(project_id=1)
# or
variables = project.variables.list()
# end var list

# var get
var = gl.project_variables.get(var_key, project_id=1)
# or
var = project.variables.get(var_key)
# end var get

# var create
var = gl.project_variables.create({'key': 'key1', 'value': 'value1'},
                                  project_id=1)
# or
var = project.variables.create({'key': 'key1', 'value': 'value1'})
# end var create

# var update
var.value = 'new_value'
var.save()
# end var update

# var delete
gl.project_variables.delete(var_key)
# or
project.variables.delete()
# or
var.delete()
# end var delete

# trigger list
triggers = gl.project_triggers.list(project_id=1)
# or
triggers = project.triggers.list()
# end trigger list

# trigger get
trigger = gl.project_triggers.get(trigger_token, project_id=1)
# or
trigger = project.triggers.get(trigger_token)
# end trigger get

# trigger create
trigger = gl.project_triggers.create({}, project_id=1)
# or
trigger = project.triggers.create({})
# end trigger create

# trigger delete
gl.project_triggers.delete(trigger_token)
# or
project.triggers.delete()
# or
trigger.delete()
# end trigger delete

# list
builds = gl.project_builds.list(project_id=1)
# or
builds = project.builds.list()
# end list

# commit list
commit = gl.project_commits.get(commit_sha, project_id=1)
builds = commit.builds()
# end commit list

# get
build = gl.project_builds.get(build_id, project_id=1)
# or
project.builds.get(build_id)
# end get

# artifacts
build.artifacts()
# end artifacts

# stream artifacts
class Foo(object):
    def __init__(self):
        self._fd = open('artifacts.zip', 'wb')

    def __call__(self, chunk):
        self._fd.write(chunk)

target = Foo()
build.artifacts(streamed=True, action=target)
del(target)  # flushes data on disk
# end stream artifacts

# keep artifacts
build.keep_artifacts()
# end keep artifacts

# trace
build.trace()
# end trace

# retry
build.cancel()
build.retry()
# end retry

# erase
build.erase()
# end erase

# play
build.play()
# end play

# trigger run
p = gl.projects.get(project_id)
p.trigger_build('master', trigger_token,
                {'extra_var1': 'foo', 'extra_var2': 'bar'})
# end trigger run

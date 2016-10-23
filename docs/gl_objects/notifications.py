# get
# global settings
settings = gl.notificationsettings.get()
# for a group
settings = gl.groups.get(group_id).notificationsettings.get()
# for a project
settings = gl.projects.get(project_id).notificationsettings.get()
# end get

# update
# use a predefined level
settings.level = gitlab.NOTIFICATION_LEVEL_WATCH
# create a custom setup
settings.level = gitlab.NOTIFICATION_LEVEL_CUSTOM
settings.save()  # will create additional attributes, but not mandatory

settings.new_merge_request = True
settings.new_issue = True
settings.new_note = True
settings.save()
# end update

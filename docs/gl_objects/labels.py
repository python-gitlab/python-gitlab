# list
labels = gl.project_labels.list(project_id=1)
# or
labels = project.labels.list()
# end list

# get
label = gl.project_labels.get(label_name, project_id=1)
# or
label = project.labels.get(label_name)
# end get

# create
label = gl.project_labels.create({'name': 'foo', 'color': '#8899aa'},
                                 project_id=1)
# or
label = project.labels.create({'name': 'foo', 'color': '#8899aa'})
# end create

# update
# change the name of the label:
label.new_name = 'bar'
label.save()
# change its color:
label.color = '#112233'
label.save()
# end update

# delete
gl.project_labels.delete(label_id, project_id=1)
# or
project.labels.delete(label_id)
# or
label.delete()
# end delete

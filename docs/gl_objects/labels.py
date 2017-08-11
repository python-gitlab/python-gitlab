# list
labels = project.labels.list()
# end list

# get
label = project.labels.get(label_name)
# end get

# create
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
project.labels.delete(label_id)
# or
label.delete()
# end delete

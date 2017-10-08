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

# use
# Labels are defined as lists in issues and merge requests. The labels must
# exist.
issue = p.issues.create({'title': 'issue title',
                         'description': 'issue description',
                         'labels': ['foo']})
issue.labels.append('bar')
issue.save()
# end use

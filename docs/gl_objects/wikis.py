# list
pages = project.wikis.list()
# end list

# get
page = project.wikis.get(page_slug)
# end get

# create
page = project.wikis.create({'title': 'Wiki Page 1',
                             'content': open(a_file).read()})
# end create

# update
page.content = 'My new content'
page.save()
# end update

# delete
page.delete()
# end delete

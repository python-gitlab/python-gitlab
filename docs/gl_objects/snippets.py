# list
snippets = gl.snippets.list()
# end list

# public list
public_snippets = gl.snippets.public()
# end public list

# get
snippet = gl.snippets.get(snippet_id)
# get the content
content = snippet.raw()
# end get

# create
snippet = gl.snippets.create({'title': 'snippet1',
                              'file_name': 'snippet1.py',
                              'content': open('snippet1.py').read()})
# end create

# update
snippet.visibility_level = gitlab.Project.VISIBILITY_PUBLIC
snippet.save()
# end update

# delete
gl.snippets.delete(snippet_id)
# or
snippet.delete()
# end delete

# list
licenses = gl.licenses.list()
# end list

# get
license = gl.licenses.get('apache-2.0', project='foobar', fullname='John Doe')
print(license.content)
# end get

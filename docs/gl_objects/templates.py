# license list
licenses = gl.licenses.list()
# end license list

# license get
license = gl.licenses.get('apache-2.0', project='foobar', fullname='John Doe')
print(license.content)
# end license get

# gitignore list
gitignores = gl.gitignores.list()
# end gitignore list

# gitignore get
gitignore = gl.gitignores.get('Python')
print(gitignore.content)
# end gitignore get

# gitlabciyml list
gitlabciymls = gl.gitlabciymls.list()
# end gitlabciyml list

# gitlabciyml get
gitlabciyml = gl.gitlabciymls.get('Pelican')
print(gitlabciyml.content)
# end gitlabciyml get

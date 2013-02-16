## Python GitLab

python-gitlab is a Python module providing access to the GitLab server API.

It supports the v3 api of GitLab.

## Requirements

Only Python 2 is supported for the moment.

python-gitlab depends on [python-requests](http://docs.python-requests.org/en/latest/).

## State

python-gitlab is a work in progress, although already usable. Changes in the API might happen.

## ToDo

* Improve documentation
* Write unit tests
* Write a command line tool to access GitLab servers

## Code snippet

`````python
# See https://github.com/gitlabhq/gitlabhq/tree/master/doc/api for the source.

# Register a connection to a gitlab instance, using its URL and a user private
# token
gl = Gitlab('http://192.168.123.107', 'JVNSESs8EwWRx5yDxM5q')
# Connect to get the current user
gl.auth()
# Print the user informations
print gl.user

# Get a list of projects
for p in gl.Project():
    print (p.name)
    # get associated issues
    issues = p.Issue()
    for issue in issues:
        closed = 0 if not issue.closed else 1
        print ("  %d => %s (closed: %d)" % (issue.id, issue.title, closed))
        # and close them all
        issue.closed = 1
        issue.save()

# Get the first 10 groups (pagination)
for g in gl.Group(page=1, per_page=10):
    print (g)

# Create a new project
p = gl.Project({'name': 'myCoolProject', 'wiki_enabled': False})
p.save()
print p
`````


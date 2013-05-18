## Python GitLab

python-gitlab is a Python module providing access to the GitLab server API.

It supports the v3 api of GitLab.

A CLI tool is also provided (called **gitlab**).

## Requirements

Only Python 2 is supported for the moment.

python-gitlab depends on [python-requests](http://docs.python-requests.org/en/latest/).

## State

python-gitlab is a work in progress, although already usable. Changes in the API might happen.

## ToDo

* Improve documentation
* Write unit tests
* Improve the command line tool

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

## Command line use

To use the command line tool, you need to define which GitLab server(s) can be
accessed. this can be done in 2 files:

* /etc/python-gitlab.cfg
* ~/.python-gitlab.cfg

Here's an example of the syntax:

`````
[global]
default = local

[local]
url = http://10.0.3.2:8080
private_token = vTbFeqJYCY3sibBP7BZM

[distant]
url = https://some.whe.re
private_token = thisisaprivatetoken
`````

The [global] section define which server is accesed by default.
Each other section defines how to access a server. Only private token
authentication is supported (not user/password).

Choosing a different server than the default one can be done at run time:

`````
gitlab --gitlab=distant [command]
`````

gitlab always requires 2 mandatory arguments.

The first argument is the object type on which we will act, the second one is
the action:

`````
gitlab Project list
`````

The usable objects are those which inherits GitlabObject (yes, the source is
the doc ATM), and the actions are list, get, create, update, delete.

Some examples:

`````bash
# list all the projects:
gitlab Project list

# get a specific project (id 2):
gitlab Project get 2

# get a list of snippets for this project:
gitlab ProjectIssue list project_id=2
# (you're right, this syntax sucks)

# delete a Snippet (id 3):
gitlab ProjectSnippet delete 3 project_id=2

# update a Snippet:
gitlab ProjectSnippet update 4 project_id=2 code="My New Code"

# create a Snippet:
gitlab ProjectSnippet create project_id=2
Impossible to create object (Missing attribute(s): title, file_name, code)

# oops, let's add the attributes:
gitlab ProjectSnippet create project_id=2 title="the title" file_name="the name" code="the code"
`````

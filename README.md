## Python GitLab

python-gitlab is a Python package providing access to the GitLab server API.

It supports the v3 api of GitLab.

A CLI tool is also provided (called **gitlab**).

## Installation

### Requirements

python-gitlab depends on:

* [python-requests](http://docs.python-requests.org/en/latest/)
* [six](https://pythonhosted.org/six/)

### Install with pip

`````
pip install python-gitlab
`````

## State

python-gitlab is considered stable.

## Bug reports

Please report bugs and feature requests at
https://github.com/gpocentek/python-gitlab/issues

## Documentation

Work In Progress: http://python-gitlab.readthedocs.org/en/latest/

Patches are welcome!

## Code snippet

`````python
# See https://github.com/gitlabhq/gitlabhq/tree/master/doc/api for the source.
from gitlab import Gitlab

# Register a connection to a gitlab instance, using its URL and a user private
# token
gl = Gitlab('http://192.168.123.107', 'JVNSESs8EwWRx5yDxM5q')
# Connect to get the current user
gl.auth()
# Print the user informations
print(gl.user)

# Get a list of projects
for p in gl.projects.list():
    print(p.name)
    # get associated issues
    issues = p.issues.list()
    for issue in issues:
        closed = 0 if not issue.closed else 1
        print("  %d => %s (closed: %d)" % (issue.id, issue.title, closed))
        # and close them all
        issue.state_event = "close"
        issue.save()

# Get the first 10 groups (pagination)
for g in gl.groups.list(page=1, per_page=10):
    print(g)

# To use pagination and retrieve all the items
for g in gl.groups.list(all=True):
    print(g)

# Create a new project (as another_user)
p = gl.project.create({'name': 'myCoolProject', 'wiki_enabled': False},
                      sudo="another_user")
print(p)
`````

## Command line use

To use the command line tool, you need to define which GitLab server(s) can be
accessed. This can be done in 2 files:

* /etc/python-gitlab.cfg
* ~/.python-gitlab.cfg

Here's an example of the syntax:

`````
[global]
# required setting
default = local

# optional settings
ssl_verify = true
timeout = 5

[local]
url = http://10.0.3.2:8080
# get the private token from the gitlab web interface
private_token = vTbFeqJYCY3sibBP7BZM

[remote]
url = https://some.whe.re
private_token = thisisaprivatetoken
ssl_verify = false
`````

The [global] section defines which server is accessed by default.
Each other section defines how to access a server. Only private token
authentication is supported (not user/password).

The `ssl_verify` option defines if the server SSL certificate should be
validated (use false for self signed certificates, only useful with https).

The `timeout` option defines after how many seconds a request to the Gitlab
server should be abandonned.

You can choose a different server than the default one at run time:

`````
gitlab --gitlab remote [command]
`````

gitlab always requires 2 mandatory arguments.

The first argument is the object type on which the program will act, the second
one is the action:

`````
gitlab project list
`````

Get help with:

`````
# global help
gitlab --help

# object help
gitlab project --help
`````

Some examples:

`````bash
# list all the projects:
gitlab project list

# limit to 5 items per request, display the 1st page only
gitlab project list --page 1 --per-page 5

# get a specific project (id 2):
gitlab project get --id 2

# get a list of snippets for this project:
gitlab project-issue list --project-id 2

# delete a Snippet (id 3):
gitlab project-snippet delete --id 3 --project-id 2

# update a Snippet:
gitlab project-snippet update --id 4 --project-id 2 --code "My New Code"

# create a Snippet:
gitlab project-snippet create --project-id 2
Impossible to create object (Missing attribute(s): title, file-name, code)

# oops, let's add the attributes:
gitlab project-snippet create --project-id 2 --title "the title" --file-name "the name" --code "the code"
`````

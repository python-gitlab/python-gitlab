== Tests

Running the tests requires to have a GitLab 4.2 server available, with a
default installation (only one admin user created, no projects, no groups...).

You need to reset the database on the test server every time the tests are run:

`````
sudo su - gitlab
cd gitlab
bundle exec rake gitlab:setup RAILS_ENV=production
`````

Run tests with:
`````
python main.py
`````

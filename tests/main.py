#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
import unittest

from gitlab import *

url = "http://192.168.123.2:8080"
email = "admin@local.host"
password = "5iveL!fe"

class AuthenticationTest(unittest.TestCase):
    def test_connect(self):
        gl = Gitlab("http://fakeurl", email=email, password=password)
        with self.assertRaises(GitlabConnectionError):
            gl.auth()

    def test_credential(self):
        gl = Gitlab(url)
        with self.assertRaises(GitlabAuthenticationError):
            gl.auth()

        gl.setCredentials(email, password)
        gl.auth()
        self.assertIsInstance(gl.user, CurrentUser)

    def test_token(self):
        gl = Gitlab(url, "fakeToken")
        with self.assertRaises(GitlabAuthenticationError):
            gl.auth()

        gl = Gitlab(url, email=email, password=password)
        gl.auth()
        token = gl.user.private_token

        gl = Gitlab(url, token)
        gl.auth()
        self.assertIsInstance(gl.user, CurrentUser)


class GitlabTest(unittest.TestCase):
    def setUp(self):
        self.gl = Gitlab(url, email=email, password=password)
        self.gl.auth()

    def test_gitlab_projects(self):
        p_list = self.gl.Project()
        self.assertEqual(len(p_list), 0)

        p = self.gl.Project({'name': 'TestProject1'})
        p.save()
        self.assertEqual(p.name, 'TestProject1')
        p_list = self.gl.Project()
        self.assertEqual(len(p_list), 1)
        self.assertEqual(p_list[0].name, p.name)

        i = p_list[0].id

        p = self.gl.Project(i)
        self.assertEqual(p.name, 'TestProject1')

    def test_gitlab_groups(self):
        g_list = self.gl.Group()
        self.assertEqual(len(g_list), 0)

        g = self.gl.Group({'name': 'TestGroup1', 'path': 'testgroup1'})
        g.save()
        self.assertEqual(g.name, 'TestGroup1')
        g_list = self.gl.Group()
        self.assertEqual(len(g_list), 1)
        self.assertEqual(g_list[0].name, g.name)

        i = g_list[0].id

        g = self.gl.Group(i)
        self.assertEqual(g.name, 'TestGroup1')

    def test_gitlab_users(self):
        u_list = self.gl.User()
        self.assertEqual(len(u_list), 1)

        u = self.gl.User({'email': 'testuser1@local.host',
                          'name': 'TestUser1',
                          'username': 'testuser1',
                          'password': 'ThePassword'})
        u.save()
        self.assertEqual(u.skype, None)
        u_list = self.gl.User()
        self.assertEqual(len(u_list), 2)
        self.assertEqual(u_list[1].name, u.name)

        i = u_list[1].id

        u = self.gl.User(i)
        self.assertEqual(u.name, 'TestUser1')

        u.skype = 'skypeaccount'
        u.save()

        u = self.gl.User(i)
        self.assertEqual(u.skype, 'skypeaccount')

        u.delete()
        u_list = self.gl.User()
        self.assertEqual(len(u_list), 1)

    def test_gitlab_issues(self):
        i_list = self.gl.Issue()
        self.assertEqual(len(i_list), 0)


if __name__ == '__main__':
    unittest.main()

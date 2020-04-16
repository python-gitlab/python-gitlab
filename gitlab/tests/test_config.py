# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest

import mock
import io

from gitlab import config


valid_config = u"""[global]
default = one
ssl_verify = true
timeout = 2

[one]
url = http://one.url
private_token = ABCDEF

[two]
url = https://two.url
private_token = GHIJKL
ssl_verify = false
timeout = 10

[three]
url = https://three.url
private_token = MNOPQR
ssl_verify = /path/to/CA/bundle.crt
per_page = 50

[four]
url = https://four.url
oauth_token = STUV
"""

no_default_config = u"""[global]
[there]
url = http://there.url
private_token = ABCDEF
"""

missing_attr_config = u"""[global]
[one]
url = http://one.url

[two]
private_token = ABCDEF

[three]
meh = hem

[four]
url = http://four.url
private_token = ABCDEF
per_page = 200
"""


class TestEnvConfig(unittest.TestCase):
    def test_env_present(self):
        with mock.patch.dict(os.environ, {"PYTHON_GITLAB_CFG": "/some/path"}):
            self.assertEqual(["/some/path"], config._env_config())

    def test_env_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual([], config._env_config())


class TestConfigParser(unittest.TestCase):
    @mock.patch("os.path.exists")
    def test_missing_config(self, path_exists):
        path_exists.return_value = False
        with self.assertRaises(config.GitlabConfigMissingError):
            config.GitlabConfigParser("test")

    @mock.patch("os.path.exists")
    @mock.patch("builtins.open")
    def test_invalid_id(self, m_open, path_exists):
        fd = io.StringIO(no_default_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        path_exists.return_value = True
        config.GitlabConfigParser("there")
        self.assertRaises(config.GitlabIDError, config.GitlabConfigParser)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        self.assertRaises(
            config.GitlabDataError, config.GitlabConfigParser, gitlab_id="not_there"
        )

    @mock.patch("os.path.exists")
    @mock.patch("builtins.open")
    def test_invalid_data(self, m_open, path_exists):
        fd = io.StringIO(missing_attr_config)
        fd.close = mock.Mock(return_value=None, side_effect=lambda: fd.seek(0))
        m_open.return_value = fd
        path_exists.return_value = True

        config.GitlabConfigParser("one")
        config.GitlabConfigParser("one")
        self.assertRaises(
            config.GitlabDataError, config.GitlabConfigParser, gitlab_id="two"
        )
        self.assertRaises(
            config.GitlabDataError, config.GitlabConfigParser, gitlab_id="three"
        )
        with self.assertRaises(config.GitlabDataError) as emgr:
            config.GitlabConfigParser("four")
        self.assertEqual("Unsupported per_page number: 200", emgr.exception.args[0])

    @mock.patch("os.path.exists")
    @mock.patch("builtins.open")
    def test_valid_data(self, m_open, path_exists):
        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        path_exists.return_value = True

        cp = config.GitlabConfigParser()
        self.assertEqual("one", cp.gitlab_id)
        self.assertEqual("http://one.url", cp.url)
        self.assertEqual("ABCDEF", cp.private_token)
        self.assertEqual(None, cp.oauth_token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual(True, cp.ssl_verify)
        self.assertIsNone(cp.per_page)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.GitlabConfigParser(gitlab_id="two")
        self.assertEqual("two", cp.gitlab_id)
        self.assertEqual("https://two.url", cp.url)
        self.assertEqual("GHIJKL", cp.private_token)
        self.assertEqual(None, cp.oauth_token)
        self.assertEqual(10, cp.timeout)
        self.assertEqual(False, cp.ssl_verify)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.GitlabConfigParser(gitlab_id="three")
        self.assertEqual("three", cp.gitlab_id)
        self.assertEqual("https://three.url", cp.url)
        self.assertEqual("MNOPQR", cp.private_token)
        self.assertEqual(None, cp.oauth_token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual("/path/to/CA/bundle.crt", cp.ssl_verify)
        self.assertEqual(50, cp.per_page)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.GitlabConfigParser(gitlab_id="four")
        self.assertEqual("four", cp.gitlab_id)
        self.assertEqual("https://four.url", cp.url)
        self.assertEqual(None, cp.private_token)
        self.assertEqual("STUV", cp.oauth_token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual(True, cp.ssl_verify)

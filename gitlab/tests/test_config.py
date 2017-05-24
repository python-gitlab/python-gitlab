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

try:
    import unittest
except ImportError:
    import unittest2 as unittest

import mock
import six

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
"""


class TestConfigParser(unittest.TestCase):
    @mock.patch('six.moves.builtins.open')
    def test_invalid_id(self, m_open):
        fd = six.StringIO(no_default_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        self.assertRaises(config.GitlabIDError, config.GitlabConfigParser)

        fd = six.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        self.assertRaises(config.GitlabDataError,
                          config.GitlabConfigParser,
                          gitlab_id='not_there')

    @mock.patch('six.moves.builtins.open')
    def test_invalid_data(self, m_open):
        fd = six.StringIO(missing_attr_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        self.assertRaises(config.GitlabDataError, config.GitlabConfigParser,
                          gitlab_id='one')
        self.assertRaises(config.GitlabDataError, config.GitlabConfigParser,
                          gitlab_id='two')
        self.assertRaises(config.GitlabDataError, config.GitlabConfigParser,
                          gitlab_id='three')

    @mock.patch('six.moves.builtins.open')
    def test_valid_data(self, m_open):
        fd = six.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd

        cp = config.GitlabConfigParser()
        self.assertEqual("one", cp.gitlab_id)
        self.assertEqual("http://one.url", cp.url)
        self.assertEqual("ABCDEF", cp.token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual(True, cp.ssl_verify)

        fd = six.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.GitlabConfigParser(gitlab_id="two")
        self.assertEqual("two", cp.gitlab_id)
        self.assertEqual("https://two.url", cp.url)
        self.assertEqual("GHIJKL", cp.token)
        self.assertEqual(10, cp.timeout)
        self.assertEqual(False, cp.ssl_verify)

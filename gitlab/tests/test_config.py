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
from textwrap import dedent

import mock
import io

from gitlab import config, USER_AGENT
import pytest


custom_user_agent = "my-package/1.0.0"

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

custom_user_agent_config = """[global]
default = one
user_agent = {}

[one]
url = http://one.url
private_token = ABCDEF
""".format(
    custom_user_agent
)

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


@mock.patch.dict(os.environ, {"PYTHON_GITLAB_CFG": "/some/path"})
def test_env_config_present():
    assert ["/some/path"] == config._env_config()


@mock.patch.dict(os.environ, {}, clear=True)
def test_env_config_missing():
    assert [] == config._env_config()


@mock.patch("os.path.exists")
def test_missing_config(path_exists):
    path_exists.return_value = False
    with pytest.raises(config.GitlabConfigMissingError):
        config.GitlabConfigParser("test")


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
def test_invalid_id(m_open, path_exists):
    fd = io.StringIO(no_default_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    path_exists.return_value = True
    config.GitlabConfigParser("there")
    with pytest.raises(config.GitlabIDError):
        config.GitlabConfigParser()

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    with pytest.raises(config.GitlabDataError):
        config.GitlabConfigParser(gitlab_id="not_there")


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
def test_invalid_data(m_open, path_exists):
    fd = io.StringIO(missing_attr_config)
    fd.close = mock.Mock(return_value=None, side_effect=lambda: fd.seek(0))
    m_open.return_value = fd
    path_exists.return_value = True

    config.GitlabConfigParser("one")
    config.GitlabConfigParser("one")
    with pytest.raises(config.GitlabDataError):
        config.GitlabConfigParser(gitlab_id="two")
    with pytest.raises(config.GitlabDataError):
        config.GitlabConfigParser(gitlab_id="three")
    with pytest.raises(config.GitlabDataError) as emgr:
        config.GitlabConfigParser("four")
    assert "Unsupported per_page number: 200" == emgr.value.args[0]


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
def test_valid_data(m_open, path_exists):
    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    path_exists.return_value = True

    cp = config.GitlabConfigParser()
    assert "one" == cp.gitlab_id
    assert "http://one.url" == cp.url
    assert "ABCDEF" == cp.private_token
    assert None == cp.oauth_token
    assert 2 == cp.timeout
    assert True == cp.ssl_verify
    assert cp.per_page is None

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="two")
    assert "two" == cp.gitlab_id
    assert "https://two.url" == cp.url
    assert "GHIJKL" == cp.private_token
    assert None == cp.oauth_token
    assert 10 == cp.timeout
    assert False == cp.ssl_verify

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="three")
    assert "three" == cp.gitlab_id
    assert "https://three.url" == cp.url
    assert "MNOPQR" == cp.private_token
    assert None == cp.oauth_token
    assert 2 == cp.timeout
    assert "/path/to/CA/bundle.crt" == cp.ssl_verify
    assert 50 == cp.per_page

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="four")
    assert "four" == cp.gitlab_id
    assert "https://four.url" == cp.url
    assert None == cp.private_token
    assert "STUV" == cp.oauth_token
    assert 2 == cp.timeout
    assert True == cp.ssl_verify


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
def test_data_from_helper(m_open, path_exists, tmp_path):
    helper = (tmp_path / "helper.sh")
    helper.write_text(dedent("""\
        #!/bin/sh
        echo "secret"
    """))
    helper.chmod(0o755)

    fd = io.StringIO(dedent("""\
        [global]
        default = helper

        [helper]
        url = https://helper.url
        oauth_token = helper: %s
    """) % helper)

    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="helper")
    assert "helper" == cp.gitlab_id
    assert "https://helper.url" == cp.url
    assert None == cp.private_token
    assert "secret" == cp.oauth_token


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
@pytest.mark.parametrize(
    "config_string,expected_agent",
    [
        (valid_config, USER_AGENT),
        (custom_user_agent_config, custom_user_agent),
    ],
)
def test_config_user_agent(m_open, path_exists, config_string, expected_agent):
    fd = io.StringIO(config_string)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd

    cp = config.GitlabConfigParser()
    assert cp.user_agent == expected_agent

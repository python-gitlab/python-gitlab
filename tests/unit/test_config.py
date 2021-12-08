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

import io
import os
import sys
from textwrap import dedent
from unittest import mock

import pytest

import gitlab
from gitlab import config

custom_user_agent = "my-package/1.0.0"

valid_config = """[global]
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

custom_user_agent_config = f"""[global]
default = one
user_agent = {custom_user_agent}

[one]
url = http://one.url
private_token = ABCDEF
"""

no_default_config = """[global]
[there]
url = http://there.url
private_token = ABCDEF
"""

missing_attr_config = """[global]
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


def global_retry_transient_errors(value: bool) -> str:
    return f"""[global]
default = one
retry_transient_errors={value}
[one]
url = http://one.url
private_token = ABCDEF"""


def global_and_gitlab_retry_transient_errors(
    global_value: bool, gitlab_value: bool
) -> str:
    return f"""[global]
    default = one
    retry_transient_errors={global_value}
    [one]
    url = http://one.url
    private_token = ABCDEF
    retry_transient_errors={gitlab_value}"""


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
    assert cp.oauth_token is None
    assert 2 == cp.timeout
    assert cp.ssl_verify is True
    assert cp.per_page is None

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="two")
    assert "two" == cp.gitlab_id
    assert "https://two.url" == cp.url
    assert "GHIJKL" == cp.private_token
    assert cp.oauth_token is None
    assert 10 == cp.timeout
    assert cp.ssl_verify is False

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="three")
    assert "three" == cp.gitlab_id
    assert "https://three.url" == cp.url
    assert "MNOPQR" == cp.private_token
    assert cp.oauth_token is None
    assert 2 == cp.timeout
    assert "/path/to/CA/bundle.crt" == cp.ssl_verify
    assert 50 == cp.per_page

    fd = io.StringIO(valid_config)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="four")
    assert "four" == cp.gitlab_id
    assert "https://four.url" == cp.url
    assert cp.private_token is None
    assert "STUV" == cp.oauth_token
    assert 2 == cp.timeout
    assert cp.ssl_verify is True


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
@pytest.mark.skipif(sys.platform.startswith("win"), reason="Not supported on Windows")
def test_data_from_helper(m_open, path_exists, tmp_path):
    helper = tmp_path / "helper.sh"
    helper.write_text(
        dedent(
            """\
            #!/bin/sh
            echo "secret"
            """
        )
    )
    helper.chmod(0o755)

    fd = io.StringIO(
        dedent(
            f"""\
            [global]
            default = helper

            [helper]
            url = https://helper.url
            oauth_token = helper: {helper}
            """
        )
    )

    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd
    cp = config.GitlabConfigParser(gitlab_id="helper")
    assert "helper" == cp.gitlab_id
    assert "https://helper.url" == cp.url
    assert cp.private_token is None
    assert "secret" == cp.oauth_token


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
@pytest.mark.parametrize(
    "config_string,expected_agent",
    [
        (valid_config, gitlab.const.USER_AGENT),
        (custom_user_agent_config, custom_user_agent),
    ],
)
def test_config_user_agent(m_open, path_exists, config_string, expected_agent):
    fd = io.StringIO(config_string)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd

    cp = config.GitlabConfigParser()
    assert cp.user_agent == expected_agent


@mock.patch("os.path.exists")
@mock.patch("builtins.open")
@pytest.mark.parametrize(
    "config_string,expected",
    [
        pytest.param(valid_config, False, id="default_value"),
        pytest.param(
            global_retry_transient_errors(True), True, id="global_config_true"
        ),
        pytest.param(
            global_retry_transient_errors(False), False, id="global_config_false"
        ),
        pytest.param(
            global_and_gitlab_retry_transient_errors(False, True),
            True,
            id="gitlab_overrides_global_true",
        ),
        pytest.param(
            global_and_gitlab_retry_transient_errors(True, False),
            False,
            id="gitlab_overrides_global_false",
        ),
        pytest.param(
            global_and_gitlab_retry_transient_errors(True, True),
            True,
            id="gitlab_equals_global_true",
        ),
        pytest.param(
            global_and_gitlab_retry_transient_errors(False, False),
            False,
            id="gitlab_equals_global_false",
        ),
    ],
)
def test_config_retry_transient_errors_when_global_config_is_set(
    m_open, path_exists, config_string, expected
):
    fd = io.StringIO(config_string)
    fd.close = mock.Mock(return_value=None)
    m_open.return_value = fd

    cp = config.GitlabConfigParser()
    assert cp.retry_transient_errors == expected

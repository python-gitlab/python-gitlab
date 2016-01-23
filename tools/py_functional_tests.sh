#!/bin/bash
# Copyright (C) 2015 Gauvain Pocentek <gauvain@pocentek.net>
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

cleanup() {
    rm -f /tmp/python-gitlab.cfg
    docker kill gitlab-test >/dev/null 2>&1
    docker rm gitlab-test >/dev/null 2>&1
    deactivate || true
    rm -rf $VENV
}
trap cleanup EXIT

setenv_script=$(dirname $0)/build_test_env.sh

. $setenv_script "$@"

VENV=$(pwd)/.venv

$VENV_CMD $VENV
. $VENV/bin/activate
pip install -rrequirements.txt
pip install -e .

sleep 10

python $(dirname $0)/python_test.py

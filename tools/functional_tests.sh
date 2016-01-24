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

CONFIG=/tmp/python-gitlab.cfg
GITLAB="gitlab --config-file $CONFIG"
GREEN='\033[0;32m'
NC='\033[0m'
OK="echo -e ${GREEN}OK${NC}"

VENV=$(pwd)/.venv

$VENV_CMD $VENV
. $VENV/bin/activate
pip install -rrequirements.txt
pip install -e .

# NOTE(gpocentek): the first call might fail without a little delay
sleep 20

set -e

echo -n "Testing project creation... "
PROJECT_ID=$($GITLAB project create --name test-project1 | grep ^id: | cut -d' ' -f2)
$GITLAB project list | grep -q test-project1
$OK

echo -n "Testing project update... "
$GITLAB project update --id $PROJECT_ID --description "My New Description"
$OK

echo -n "Testing user creation... "
USER_ID=$($GITLAB user create --email fake@email.com --username user1 --name "User One" --password fakepassword | grep ^id: | cut -d' ' -f2)
$OK

echo -n "Testing verbose output... "
$GITLAB -v user list | grep -q avatar-url
$OK

echo -n "Testing CLI args not in output... "
$GITLAB -v user list | grep -qv config-file
$OK

echo -n "Testing adding member to a project... "
$GITLAB project-member create --project-id $PROJECT_ID --user-id $USER_ID --access-level 40 >/dev/null 2>&1
$OK

echo -n "Testing file creation... "
$GITLAB project-file create --project-id $PROJECT_ID --file-path README --branch-name master --content "CONTENT" --commit-message "Initial commit" >/dev/null 2>&1
$OK

echo -n "Testing issue creation... "
ISSUE_ID=$($GITLAB project-issue create --project-id $PROJECT_ID --title "my issue" --description "my issue description" | grep ^id: | cut -d' ' -f2)
$OK

echo -n "Testing note creation... "
$GITLAB project-issue-note create --project-id $PROJECT_ID --issue-id $ISSUE_ID --body "the body" >/dev/null 2>&1
$OK

echo -n "Testing branch creation... "
$GITLAB project-branch create --project-id $PROJECT_ID --branch-name branch1 --ref master >/dev/null 2>&1
$OK

echo -n "Testing branch deletion... "
$GITLAB project-branch delete --project-id $PROJECT_ID --name branch1 >/dev/null 2>&1
$OK

echo -n "Testing project deletion... "
$GITLAB project delete --id $PROJECT_ID
$OK

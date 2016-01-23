#!/bin/sh
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

setenv_script=$(dirname "$0")/build_test_env.sh || exit 1
BUILD_TEST_ENV_AUTO_CLEANUP=true
. "$setenv_script" "$@" || exit 1

printf %s "Testing project creation... "
OUTPUT=$(try GITLAB project create --name test-project1) || exit 1
PROJECT_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)
OUTPUT=$(try GITLAB project list) || exit 1
pecho "${OUTPUT}" | grep -q test-project1 || fatal "test failed"
OK

printf %s "Testing project update... "
GITLAB project update --id "$PROJECT_ID" --description "My New Description" \
    || fatal "test failed"
OK

printf %s "Testing user creation... "
OUTPUT=$(GITLAB user create --email fake@email.com --username user1 \
    --name "User One" --password fakepassword) || fatal "test failed"
OK
USER_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)

printf %s "Testing verbose output... "
OUTPUT=$(try GITLAB -v user list) || exit 1
pecho "${OUTPUT}" | grep -q avatar-url || fatal "test failed"
OK

printf %s "Testing CLI args not in output... "
OUTPUT=$(try GITLAB -v user list) || exit 1
pecho "${OUTPUT}" | grep -qv config-file || fatal "test failed"
OK

printf %s "Testing adding member to a project... "
GITLAB project-member create --project-id "$PROJECT_ID" \
    --user-id "$USER_ID" --access-level 40 >/dev/null 2>&1 \
    || fatal "test failed"
OK

printf %s "Testing file creation... "
GITLAB project-file create --project-id "$PROJECT_ID" \
    --file-path README --branch-name master --content "CONTENT" \
    --commit-message "Initial commit" >/dev/null 2>&1 || fatal "test failed"
OK

printf %s "Testing issue creation... "
OUTPUT=$(GITLAB project-issue create --project-id "$PROJECT_ID" \
    --title "my issue" --description "my issue description") \
    || fatal "test failed"
OK
ISSUE_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)

printf %s "Testing note creation... "
GITLAB project-issue-note create --project-id "$PROJECT_ID" \
    --issue-id "$ISSUE_ID" --body "the body" >/dev/null 2>&1 \
    || fatal "test failed"
OK

printf %s "Testing branch creation... "
GITLAB project-branch create --project-id "$PROJECT_ID" \
    --branch-name branch1 --ref master >/dev/null 2>&1 || fatal "test failed"
OK

printf %s "Testing branch deletion... "
GITLAB project-branch delete --project-id "$PROJECT_ID" \
    --name branch1 >/dev/null 2>&1 || fatal "test failed"
OK

printf %s "Testing project deletion... "
GITLAB project delete --id "$PROJECT_ID" || fatal "test failed"
OK

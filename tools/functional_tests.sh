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

testcase "project creation" '
    OUTPUT=$(try GITLAB project create --name test-project1) || exit 1
    PROJECT_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d" " -f2)
    OUTPUT=$(try GITLAB project list) || exit 1
    pecho "${OUTPUT}" | grep -q test-project1
'

testcase "project update" '
    GITLAB project update --id "$PROJECT_ID" --description "My New Description"
'

testcase "user creation" '
    OUTPUT=$(GITLAB user create --email fake@email.com --username user1 \
        --name "User One" --password fakepassword)
'
USER_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)

testcase "user get (by id)" '
    GITLAB user get --id $USER_ID >/dev/null 2>&1
'

testcase "user get (by username)" '
    GITLAB user get-by-username --query user1 >/dev/null 2>&1
'

testcase "verbose output" '
    OUTPUT=$(try GITLAB -v user list) || exit 1
    pecho "${OUTPUT}" | grep -q avatar-url
'

testcase "CLI args not in output" '
    OUTPUT=$(try GITLAB -v user list) || exit 1
    pecho "${OUTPUT}" | grep -qv config-file
'

testcase "adding member to a project" '
    GITLAB project-member create --project-id "$PROJECT_ID" \
        --user-id "$USER_ID" --access-level 40 >/dev/null 2>&1
'

testcase "file creation" '
    GITLAB project-file create --project-id "$PROJECT_ID" \
        --file-path README --branch-name master --content "CONTENT" \
        --commit-message "Initial commit" >/dev/null 2>&1
'

testcase "issue creation" '
    OUTPUT=$(GITLAB project-issue create --project-id "$PROJECT_ID" \
        --title "my issue" --description "my issue description")
'
ISSUE_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)

testcase "note creation" '
    GITLAB project-issue-note create --project-id "$PROJECT_ID" \
        --issue-id "$ISSUE_ID" --body "the body" >/dev/null 2>&1
'

testcase "branch creation" '
    GITLAB project-branch create --project-id "$PROJECT_ID" \
        --branch-name branch1 --ref master >/dev/null 2>&1
'

GITLAB project-file create --project-id "$PROJECT_ID" \
    --file-path README2 --branch-name branch1 --content "CONTENT" \
    --commit-message "second commit" >/dev/null 2>&1

testcase "merge request creation" '
    OUTPUT=$(GITLAB project-merge-request create \
        --project-id "$PROJECT_ID" \
        --source-branch branch1 --target-branch master \
        --title "Update README")
'
MR_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)

testcase "merge request validation" '
    GITLAB project-merge-request merge --project-id "$PROJECT_ID" \
        --id "$MR_ID" >/dev/null 2>&1
'

testcase "branch deletion" '
    GITLAB project-branch delete --project-id "$PROJECT_ID" \
        --name branch1 >/dev/null 2>&1
'

testcase "project deletion" '
    GITLAB project delete --id "$PROJECT_ID"
'

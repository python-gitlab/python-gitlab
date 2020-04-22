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

testcase "project creation" '
    OUTPUT=$(try GITLAB project create --name test-project1) || exit 1
    PROJECT_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d" " -f2)
    OUTPUT=$(try GITLAB project list) || exit 1
    pecho "${OUTPUT}" | grep -q test-project1
'

testcase "project update" '
    GITLAB project update --id "$PROJECT_ID" --description "My New Description"
'

testcase "group creation" '
    OUTPUT=$(try GITLAB group create --name test-group1 --path group1) || exit 1
    GROUP_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d" " -f2)
    OUTPUT=$(try GITLAB group list) || exit 1
    pecho "${OUTPUT}" | grep -q test-group1
'

testcase "group update" '
    GITLAB group update --id "$GROUP_ID" --description "My New Description"
'

testcase "user creation" '
    OUTPUT=$(GITLAB user create --email fake@email.com --username user1 \
        --name "User One" --password fakepassword)
'
USER_ID=$(pecho "${OUTPUT}" | grep ^id: | cut -d' ' -f2)

testcase "user get (by id)" '
    GITLAB user get --id $USER_ID >/dev/null 2>&1
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

testcase "listing user memberships" '
    GITLAB user-membership list --user-id "$USER_ID" >/dev/null 2>&1
'

testcase "file creation" '
    GITLAB project-file create --project-id "$PROJECT_ID" \
        --file-path README --branch master --content "CONTENT" \
        --commit-message "Initial commit" >/dev/null 2>&1
'

testcase "issue creation" '
    OUTPUT=$(GITLAB project-issue create --project-id "$PROJECT_ID" \
        --title "my issue" --description "my issue description")
'
ISSUE_ID=$(pecho "${OUTPUT}" | grep ^iid: | cut -d' ' -f2)

testcase "note creation" '
    GITLAB project-issue-note create --project-id "$PROJECT_ID" \
        --issue-iid "$ISSUE_ID" --body "the body" >/dev/null 2>&1
'

testcase "branch creation" '
    GITLAB project-branch create --project-id "$PROJECT_ID" \
        --branch branch1 --ref master >/dev/null 2>&1
'

GITLAB project-file create --project-id "$PROJECT_ID" \
    --file-path README2 --branch branch1 --content "CONTENT" \
    --commit-message "second commit" >/dev/null 2>&1

testcase "merge request creation" '
    OUTPUT=$(GITLAB project-merge-request create \
        --project-id "$PROJECT_ID" \
        --source-branch branch1 --target-branch master \
        --title "Update README")
'
MR_ID=$(pecho "${OUTPUT}" | grep ^iid: | cut -d' ' -f2)

testcase "merge request validation" '
    GITLAB project-merge-request merge --project-id "$PROJECT_ID" \
        --iid "$MR_ID" >/dev/null 2>&1
'

# Test revert commit
COMMITS=$(GITLAB -v project-commit list --project-id "${PROJECT_ID}")
COMMIT_ID=$(pecho "${COMMITS}" | grep -m1 '^id:' | cut -d' ' -f2)

testcase "revert commit" '
    GITLAB project-commit revert --project-id "$PROJECT_ID" \
        --id "$COMMIT_ID" --branch master
'

# Test commit signature
testcase "attempt to get signature of unsigned commit" '
    OUTPUT=$(GITLAB project-commit signature --project-id "$PROJECT_ID" \
        --id "$COMMIT_ID" 2>&1 || exit 0)
    echo "$OUTPUT" | grep -q "404 Signature Not Found"
'

# Test project labels
testcase "create project label" '
    OUTPUT=$(GITLAB -v project-label create --project-id $PROJECT_ID \
        --name prjlabel1 --description "prjlabel1 description" --color "#112233")
'

testcase "list project label" '
    OUTPUT=$(GITLAB -v project-label list --project-id $PROJECT_ID)
'

testcase "update project label" '
    OUTPUT=$(GITLAB -v project-label update --project-id $PROJECT_ID \
        --name prjlabel1 --new-name prjlabel2 --description "prjlabel2 description" --color "#332211")
'

testcase "delete project label" '
    OUTPUT=$(GITLAB -v project-label delete --project-id $PROJECT_ID \
        --name prjlabel2)
'

# Test group labels
testcase "create group label" '
    OUTPUT=$(GITLAB -v group-label create --group-id $GROUP_ID \
        --name grplabel1 --description "grplabel1 description" --color "#112233")
'

testcase "list group label" '
    OUTPUT=$(GITLAB -v group-label list --group-id $GROUP_ID)
'

testcase "update group label" '
    OUTPUT=$(GITLAB -v group-label update --group-id $GROUP_ID \
        --name grplabel1 --new-name grplabel2 --description "grplabel2 description" --color "#332211")
'

testcase "delete group label" '
    OUTPUT=$(GITLAB -v group-label delete --group-id $GROUP_ID \
        --name grplabel2)
'

# Test project variables
testcase "create project variable" '
    OUTPUT=$(GITLAB -v project-variable create --project-id $PROJECT_ID \
        --key junk --value car)
'

testcase "get project variable" '
    OUTPUT=$(GITLAB -v project-variable get --project-id $PROJECT_ID \
        --key junk)
'

testcase "update project variable" '
    OUTPUT=$(GITLAB -v project-variable update --project-id $PROJECT_ID \
        --key junk --value bus)
'

testcase "list project variable" '
    OUTPUT=$(GITLAB -v project-variable list --project-id $PROJECT_ID)
'

testcase "delete project variable" '
    OUTPUT=$(GITLAB -v project-variable delete --project-id $PROJECT_ID \
        --key junk)
'

testcase "branch deletion" '
    GITLAB project-branch delete --project-id "$PROJECT_ID" \
        --name branch1 >/dev/null 2>&1
'

testcase "project upload" '
    GITLAB project upload --id "$PROJECT_ID" \
        --filename '$(basename $0)' --filepath '$0' >/dev/null 2>&1
'

testcase "application settings get" '
    GITLAB application-settings get >/dev/null 2>&1
'

testcase "application settings update" '
    GITLAB application-settings update --signup-enabled false >/dev/null 2>&1
'

cat > /tmp/gitlab-project-description << EOF
Multi line

Data
EOF
testcase "values from files" '
    OUTPUT=$(GITLAB -v project create --name fromfile \
            --description @/tmp/gitlab-project-description)
    echo $OUTPUT | grep -q "Multi line"
'

# Test deploy tokens
CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v project-deploy-token create --project-id $PROJECT_ID \
        --name foo --username root --expires-at "2021-09-09" --scopes "read_registry")
CREATED_DEPLOY_TOKEN_ID=$(echo "$CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT" | grep ^id: | cut -d" " -f2)
testcase "create project deploy token" '
    echo $CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT | grep -q "name: foo"
'
testcase "create project deploy token" '
    echo $CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT | grep -q "expires-at: 2021-09-09T00:00:00.000Z"
'
testcase "create project deploy token" '
    echo $CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT | grep "scopes: " | grep -q "read_registry"
'
# Uncomment once https://gitlab.com/gitlab-org/gitlab/-/issues/211963 is fixed
#testcase "create project deploy token" '
#    echo $CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT | grep -q "username: root"
#'

# Remove once https://gitlab.com/gitlab-org/gitlab/-/issues/211963 is fixed
testcase "create project deploy token" '
    echo $CREATE_PROJECT_DEPLOY_TOKEN_OUTPUT | grep -q "gitlab+deploy-token"
'

LIST_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v deploy-token list)
testcase "list all deploy tokens" '
    echo $LIST_DEPLOY_TOKEN_OUTPUT | grep -q "name: foo"
'
testcase "list all deploy tokens" '
    echo $LIST_DEPLOY_TOKEN_OUTPUT | grep -q "id: $CREATED_DEPLOY_TOKEN_ID"
'
testcase "list all deploy tokens" '
    echo $LIST_DEPLOY_TOKEN_OUTPUT | grep -q "expires-at: 2021-09-09T00:00:00.000Z"
'
testcase "list all deploy tokens" '
    echo $LIST_DEPLOY_TOKEN_OUTPUT | grep "scopes: " | grep -q "read_registry"
'

testcase "list project deploy tokens" '
    OUTPUT=$(GITLAB -v project-deploy-token list --project-id $PROJECT_ID)
    echo $OUTPUT | grep -q "id: $CREATED_DEPLOY_TOKEN_ID"
'
testcase "delete project deploy token" '
    GITLAB -v project-deploy-token delete  --project-id $PROJECT_ID --id $CREATED_DEPLOY_TOKEN_ID
    LIST_PROJECT_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v project-deploy-token list --project-id $PROJECT_ID)
    echo $LIST_PROJECT_DEPLOY_TOKEN_OUTPUT | grep -qv "id: $CREATED_DEPLOY_TOKEN_ID"
'
# Uncomment once https://gitlab.com/gitlab-org/gitlab/-/issues/212523 is fixed
#testcase "delete project deploy token" '
#    LIST_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v deploy-token list)
#    echo $LIST_DEPLOY_TOKEN_OUTPUT | grep -qv "id: $CREATED_DEPLOY_TOKEN_ID"
#'

CREATE_GROUP_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v group-deploy-token create --group-id $GROUP_ID \
        --name bar --username root --expires-at "2021-09-09" --scopes "read_repository")
CREATED_DEPLOY_TOKEN_ID=$(echo "$CREATE_GROUP_DEPLOY_TOKEN_OUTPUT" | grep ^id: | cut -d" " -f2)
testcase "create group deploy token" '
    echo $CREATE_GROUP_DEPLOY_TOKEN_OUTPUT | grep -q "name: bar"
'
testcase "list group deploy tokens" '
    OUTPUT=$(GITLAB -v group-deploy-token list --group-id $GROUP_ID)
    echo $OUTPUT | grep -q "id: $CREATED_DEPLOY_TOKEN_ID"
'
testcase "delete group deploy token" '
    GITLAB -v group-deploy-token delete  --group-id $GROUP_ID --id $CREATED_DEPLOY_TOKEN_ID
    LIST_GROUP_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v group-deploy-token list --group-id $GROUP_ID)
    echo $LIST_GROUP_DEPLOY_TOKEN_OUTPUT | grep -qv "id: $CREATED_DEPLOY_TOKEN_ID"
'
# Uncomment once https://gitlab.com/gitlab-org/gitlab/-/issues/212523 is fixed
#testcase "delete group deploy token" '
#    LIST_DEPLOY_TOKEN_OUTPUT=$(GITLAB -v deploy-token list)
#    echo $LIST_DEPLOY_TOKEN_OUTPUT | grep -qv "id: $CREATED_DEPLOY_TOKEN_ID"
#'

testcase "project deletion" '
    GITLAB project delete --id "$PROJECT_ID"
'

testcase "group deletion" '
    OUTPUT=$(try GITLAB group delete --id $GROUP_ID)
'

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

docker run --name gitlab-test --detach --publish 8080:80 --publish 2222:22 sytse/gitlab-ce:7.10.1 >/dev/null 2>&1

LOGIN='root'
PASSWORD='5iveL!fe'
CONFIG=/tmp/python-gitlab.cfg
GITLAB="gitlab --config-file $CONFIG"
VENV=$(pwd)/.venv

virtualenv $VENV
. $VENV/bin/activate
pip install -rrequirements.txt
pip install -e .

GREEN='\033[0;32m'
NC='\033[0m'
OK="echo -e ${GREEN}OK${NC}"

echo -n "Waiting for gitlab to come online... "
I=0
while :; do
    sleep 5
    curl -s http://localhost:8080/users/sign_in 2>/dev/null | grep -q "GitLab Community Edition" && break
    let I=I+5
    [ $I -eq 120 ] && exit 1
done
sleep 5
$OK

# Get the token
TOKEN=$(curl -s http://localhost:8080/api/v3/session \
    -X POST \
    --data "login=$LOGIN&password=$PASSWORD" \
    | python -c 'import sys, json; print json.load(sys.stdin)["private_token"]')

cat > $CONFIG << EOF
[global]
default = local
timeout = 2

[local]
url = http://localhost:8080
private_token = $TOKEN
EOF

echo "Config file content ($CONFIG):"
cat $CONFIG

# NOTE(gpocentek): the first call might fail without a little delay
sleep 10

set -e

echo -n "Testing project creation... "
PROJECT_ID=$($GITLAB project create --name test-project1 | grep ^id: | cut -d' ' -f2)
$GITLAB project list | grep -q test-project1
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

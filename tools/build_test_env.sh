#!/bin/bash
# Copyright (C) 2016 Gauvain Pocentek <gauvain@pocentek.net>
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

pecho() { printf %s\\n "$*"; }
log() {
    [ "$#" -eq 0 ] || { pecho "$@"; return 0; }
    while IFS= read -r log_line || [ -n "${log_line}" ]; do
        log "${log_line}"
    done
}
error() { log "ERROR: $@" >&2; }
fatal() { error "$@"; exit 1; }
try() { "$@" || fatal "'$@' failed"; }

PY_VER=2
while getopts :p: opt "$@"; do
    case $opt in
        p) PY_VER=$OPTARG;;
        *) echo "Unknown option: $opt"; exit 1;;
    esac
done

case $PY_VER in
    2) VENV_CMD=virtualenv;;
    3) VENV_CMD=pyvenv;;
    *) echo "Wrong python version (2 or 3)"; exit 1;;
esac

VENV=$(pwd)/.venv

cleanup() {
    rm -f /tmp/python-gitlab.cfg
    docker kill gitlab-test >/dev/null 2>&1
    docker rm gitlab-test >/dev/null 2>&1
    deactivate || true
    rm -rf $VENV
}
[ -z "${BUILD_TEST_ENV_AUTO_CLEANUP+set}" ] || {
    trap cleanup EXIT
}

docker run --name gitlab-test --detach --publish 8080:80 \
    --publish 2222:22 gpocentek/test-python-gitlab:latest >/dev/null 2>&1

LOGIN='root'
PASSWORD='5iveL!fe'
CONFIG=/tmp/python-gitlab.cfg
GITLAB="gitlab --config-file $CONFIG"
GREEN='\033[0;32m'
NC='\033[0m'
OK="echo -e ${GREEN}OK${NC}"

echo -n "Waiting for gitlab to come online... "
I=0
while :; do
    sleep 5
    curl -s http://localhost:8080/users/sign_in 2>/dev/null \
        | grep -q "GitLab Community Edition" && break
    let I=I+5
    [ $I -eq 120 ] && exit 1
done
sleep 5
$OK

# Get the token
TOKEN=$(curl -s http://localhost:8080/api/v3/session \
    -X POST \
    --data "login=$LOGIN&password=$PASSWORD" \
    | python -c \
        'import sys, json; print(json.load(sys.stdin)["private_token"])')

cat > $CONFIG << EOF
[global]
default = local
timeout = 10

[local]
url = http://localhost:8080
private_token = $TOKEN
EOF

echo "Config file content ($CONFIG):"
cat $CONFIG

$VENV_CMD $VENV
. $VENV/bin/activate
pip install -rrequirements.txt
pip install -e .

sleep 20

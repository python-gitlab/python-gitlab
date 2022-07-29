#!/bin/bash

set -u

if [[ -z "${CI:-}" || -z "${GITHUB_ACTIONS:-}" ]]; then
    echo "ERROR: Not running in the GitHub CI."
    exit 2
fi

CONFIG_FILE=~/.python-gitlab.cfg
if [[ -e "${CONFIG_FILE}" ]]; then
    echo "ERROR: Config file already exists: ${CONFIG_FILE}"
    echo "Saved you from destroying your config"
    exit 2
fi

cat <<EOF >"${CONFIG_FILE}"
[global]
default = gitlab
ssl_verify = true
timeout = 5
api_version = 4

[gitlab]
url = https://gitlab.com/
private_token = not-a-valid-token
EOF

echo "Setup config at: ${CONFIG_FILE}"

#!/bin/sh

GITLAB_CFG=${GITLAB_CFG:-"/etc/python-gitlab-default.cfg"}

cat << EOF > /etc/python-gitlab-default.cfg
[global]
default = gitlab
ssl_verify = ${GITLAB_SSL_VERIFY:-true}
timeout = ${GITLAB_TIMEOUT:-5}
api_version = ${GITLAB_API_VERSION:-4}
per_page = ${GITLAB_PER_PAGE:-10}

[gitlab]
url = ${GITLAB_URL:-https://gitlab.com}
private_token = ${GITLAB_PRIVATE_TOKEN}
oauth_token = ${GITLAB_OAUTH_TOKEN}
http_username = ${GITLAB_HTTP_USERNAME}
http_password = ${GITLAB_HTTP_PASSWORD}
EOF

exec gitlab --config-file "${GITLAB_CFG}" $@

FROM python:3.7-alpine AS base

# ensure latest updates are installed (security)
RUN apk upgrade --no-cache
RUN pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install --no-cache-dir -U

WORKDIR /opt/python-gitlab


FROM base AS build

COPY . .
RUN python setup.py bdist_wheel


FROM base

COPY --from=build /opt/python-gitlab/dist/ /opt/python-gitlab/dist/

RUN pip install --no-cache-dir PyYaml
RUN pip install --no-cache-dir $(find dist -name *.whl)

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["--version"]

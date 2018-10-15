FROM python:3.7-alpine AS build

WORKDIR /opt/python-gitlab
COPY . .
RUN python setup.py bdist_wheel

FROM python:3.7-alpine

WORKDIR /opt/python-gitlab
COPY --from=build /opt/python-gitlab/dist dist/
RUN pip install $(find dist -name *.whl) && \
    rm -rf dist/
COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["--version"]

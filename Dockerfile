ARG PYTHON_FLAVOR=alpine
FROM python:3.11-${PYTHON_FLAVOR} AS build

WORKDIR /opt/python-gitlab
COPY . .
RUN pip install build && python -m build

FROM python:3.11-${PYTHON_FLAVOR}

WORKDIR /opt/python-gitlab
COPY --from=build /opt/python-gitlab/dist dist/
RUN pip install PyYaml
RUN pip install $(find dist -name *.whl) && \
    rm -rf dist/

ENTRYPOINT ["gitlab"]
CMD ["--version"]

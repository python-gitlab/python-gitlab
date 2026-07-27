ARG PYTHON_FLAVOR=alpine
FROM python:3.12-${PYTHON_FLAVOR} AS build

WORKDIR /opt/python-gitlab
COPY . .
RUN pip install --no-cache-dir build && python -m build --wheel

FROM python:3.12-${PYTHON_FLAVOR}

LABEL org.opencontainers.image.source="https://github.com/python-gitlab/python-gitlab"

WORKDIR /opt/python-gitlab
COPY --from=build /opt/python-gitlab/dist dist/
RUN pip install --no-cache-dir PyYaml
RUN pip install --no-cache-dir $(find dist -name *.whl) && \
    rm -rf dist/

ENTRYPOINT ["gitlab"]

# Run as a non-root user for container security
RUN (addgroup -S app 2>/dev/null || groupadd --system app) && (adduser -S -u 1001 -G app app 2>/dev/null || useradd --system --uid 1001 --gid app --create-home app)
USER 1001
CMD ["--version"]

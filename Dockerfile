FROM python:3.10-alpine AS build

WORKDIR /opt/python-gitlab
COPY . .
RUN python setup.py bdist_wheel

FROM python:3.10-alpine

WORKDIR /opt/python-gitlab
COPY --from=build /opt/python-gitlab/dist dist/
RUN pip install PyYaml
RUN pip install $(find dist -name *.whl) && \
    rm -rf dist/

ENTRYPOINT ["gitlab"]
CMD ["--version"]

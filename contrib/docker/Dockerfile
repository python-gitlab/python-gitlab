FROM python:alpine

RUN pip install --upgrade python-gitlab

COPY entrypoint-python-gitlab.sh /usr/local/bin/.

WORKDIR /src

ENTRYPOINT ["entrypoint-python-gitlab.sh"]
CMD ["--version"]

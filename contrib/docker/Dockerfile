FROM python:slim

# Install python-gitlab
RUN pip install --upgrade python-gitlab

# Copy sample configuration file
COPY python-gitlab.cfg /

# Define the entrypoint that enable a configuration file
ENTRYPOINT ["gitlab", "--config-file", "/python-gitlab.cfg"]

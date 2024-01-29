FROM mcr.microsoft.com/devcontainers/python:3.11

# Install basic build tools
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      iputils-ping \
      unzip \
      rsync \
      zip \
      curl

ENV LANG="C.UTF-8"

# Install projects reqs
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

WORKDIR "/goarty"

COPY . "/goarty"

# Start django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
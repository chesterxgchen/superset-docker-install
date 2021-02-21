#FROM python36:1.1.0
#FROM python:3.7.9
FROM python:3.6.12

# Superset version
ARG SUPERSET_VERSION=${SUPERSET_VERSION:-0.34.0}
ARG DEBIAN_FRONTEND=noninteractive

# Create superset user
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash superset

# Configure environment
ENV GUNICORN_BIND=0.0.0.0:8088 \
    GUNICORN_LIMIT_REQUEST_FIELD_SIZE=0 \
    GUNICORN_LIMIT_REQUEST_LINE=0 \
    GUNICORN_TIMEOUT=60 \
    GUNICORN_WORKERS=2 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONPATH=/opt/superset:$PYTHONPATH \
    SUPERSET_REPO=apache/incubator-superset \
    SUPERSET_VERSION=${SUPERSET_VERSION} \
    SUPERSET_HOME=/opt/superset \
    DEBIAN_FRONTEND=noninteractive
ENV GUNICORN_CMD_ARGS="--workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIMEOUT} --bind ${GUNICORN_BIND} --limit-request-line ${GUNICORN_LIMIT_REQUEST_LINE} --limit-request-field_size ${GUNICORN_LIMIT_REQUEST_FIELD_SIZE}"

# install dependencies
RUN apt-get update -y

# Install dependencies to fix `curl https support error` and `elaying package configuration warning`
RUN apt-get install -y apt-transport-https apt-utils

RUN rm -rf /usr/lib/python3/site-packages/pip

# Install superset dependencies
# https://superset.incubator.apache.org/installation.html#os-dependencies
RUN apt-get install -y build-essential libssl-dev \
    libffi-dev python3-dev libsasl2-dev libldap2-dev libxi-dev

# Install some useful tools
RUN apt-get install -y curl netcat

RUN apt-get install -y emacs-nox vim less default-libmysqlclient-dev redis-tools curl netcat tree
RUN apt-get install -y python3-pip python3-requests python3-boto3 python3-pyparsing
RUN pip install --upgrade setuptools pip pyyaml


# LDAP related
RUN apt-get install -y \
         default-libmysqlclient-dev \
         libldap2-dev \
         freetds-bin \
         freetds-dev \
         libffi-dev \
         libpq-dev \
         libsasl2-2 \
         libsasl2-dev \
         libsasl2-modules-gssapi-mit \
         libssl1.0

RUN  apt-get clean
RUN  rm -r /var/lib/apt/lists/*

# superset dependencies
COPY requirements.txt /opt/superset/requirements.txt
RUN pip install --no-cache-dir -r /opt/superset/requirements.txt

RUN pip install apache-superset==${SUPERSET_VERSION} && rm -rf /root/.cache/pip

COPY superset_config.py         /opt/superset/
COPY docker-entrypoint          /usr/local/bin/

RUN chown -R superset:superset  ${SUPERSET_HOME}
RUN chown -R superset:superset  /opt/superset

RUN mkdir -p /opt/superset/bin
RUN chmod -R +x /opt/superset/bin
RUN chmod +x /usr/local/bin/docker-entrypoint

RUN mkdir /var/log/superset
RUN chown -R superset:superset /var/log/superset

ENV PYTHONPATH=${PYTHONPATH}:/usr/lib/python3/dist-packages

USER superset
ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]

VOLUME /home/superset
WORKDIR /home/superset

# Deploy application
EXPOSE 8088
HEALTHCHECK CMD ["curl", "-f", "http://localhost:8088/health"]



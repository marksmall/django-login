FROM python:3.7

LABEL project "server"

ARG COMMIT_HASH="undefined"
ARG GIT_BRANCH="undefined"
ENV COMMIT_HASH=$COMMIT_HASH
ENV GIT_BRANCH=$GIT_BRANCH

ENV PROJECT_DIR=/opt/frontend-login
ENV MANAGE_PY=$PROJECT_DIR/manage.py
ENV PYTHONPATH=/usr/local/bin
ENV DJANGO_SETTINGS_MODULE=server.settings

WORKDIR $PROJECT_DIR

COPY Pipfile Pipfile.lock /

RUN apt update && apt install -y postgresql-client python3-gdal && \
  rm -rf /var/lib/apt/lists/* && \
  pip3 install --upgrade pip && \
  pip3 install --upgrade pipenv && \
  pipenv install --system --dev

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["-w"]

EXPOSE 8888:8888

COPY . .

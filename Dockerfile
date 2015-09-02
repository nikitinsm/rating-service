FROM python:2.7

COPY ./requirements.pip /srv/requirements.pip
RUN pip install -r /srv/requirements.pip

ENV APP_NAME="/rating_service"
ENV APP_ROOT="/opt${APP_NAME}"
ENV APP_REPOSITORY="${APP_ROOT}/repository"
ENV PYTHONPATH="${PYTHONPATH}:${APP_REPOSITORY}/src"

COPY . ${APP_REPOSITORY}

EXPOSE 80

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:80", "-k", "gevent", "rating_service.application"]
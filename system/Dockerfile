FROM python:3.10.10-slim-buster

WORKDIR /build/app

ENV PYTHONPATH=/build/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV POETRY_HOME=/build/poetry
ENV POETRY_VERSION=1.4.0

COPY poetry.lock pyproject.toml  /build/app/

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends wget libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && wget -O /build/install-poetry.py https://install.python-poetry.org \
    && python /build/install-poetry.py --version $POETRY_VERSION

RUN $POETRY_HOME/bin/poetry config virtualenvs.create false \
    && $POETRY_HOME/bin/poetry install --no-interaction --no-ansi --only main,uvloop

COPY . .

COPY system/entry_point*.sh /build/bin/
RUN chmod a+x /build/bin/*.sh

COPY system/gunicorn.py /opt/gunicorn.py

ARG VERSION
RUN echo ${VERSION} > version.txt

EXPOSE 80 8001

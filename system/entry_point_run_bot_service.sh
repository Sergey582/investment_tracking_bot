#!/bin/sh

set -e

export APP_MODULE="app.api.public.main:app"
export GUNICORN_CONFIG=/opt/gunicorn.py
PID=/var/run/gunicorn.pid

aerich upgrade

nohup gunicorn -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONFIG" --pid=$PID "$APP_MODULE"

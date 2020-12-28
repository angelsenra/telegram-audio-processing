#!/usr/bin/env bash

DEVELOPMENT_MODE=${DEVELOPMENT_MODE:-"0"}

if [ "${DEVELOPMENT_MODE}" = "1" ]; then
    echo "Running in reload mode!"
    echo "Starting gunicorn..."
    gunicorn --reload backend:app
else
    echo "Starting gunicorn..."
    gunicorn backend:app
fi

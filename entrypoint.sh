#!/bin/sh
set -e

exec gunicorn habit_tracker.main:create_app --workers 1 --preload --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
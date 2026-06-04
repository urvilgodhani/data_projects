#!/usr/bin/env bash
gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 live_service.app:app

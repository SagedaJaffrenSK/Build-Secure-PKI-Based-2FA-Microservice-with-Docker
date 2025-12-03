#!/usr/bin/env bash
set -e
service cron start || cron
exec uvicorn app.main:app --host 0.0.0.0 --port 8080

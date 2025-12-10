#!/bin/bash
set -euo pipefail

# register cron job
if [ -f /cron/2fa-cron ]; then
  cp /cron/2fa-cron /etc/cron.d/2fa-cron
  chmod 0644 /etc/cron.d/2fa-cron
  crontab /etc/cron.d/2fa-cron
fi

# start cron
service cron start || cron &

# ensure persistence directory
mkdir -p /data

# run API
exec python /app/main.py

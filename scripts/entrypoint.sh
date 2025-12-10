#!/bin/bash
set -euo pipefail

# register cron job if file exists
if [ -f /cron/2fa-cron ]; then
  cp /cron/2fa-cron /etc/cron.d/2fa-cron
  chmod 0644 /etc/cron.d/2fa-cron
  crontab /etc/cron.d/2fa-cron
fi

# start cron (background)
service cron start || cron &

# ensure /data exists
mkdir -p /data

# start API (use correct path to your main)
exec python /app/scripts/main.py

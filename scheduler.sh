#!/bin/sh
set -e

# Apply timezone
ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
echo "$TZ" > /etc/timezone

# Schedule the print job
echo "$CRON root /bin/sh /data/run.sh >> /data/cron.log 2>&1" > /etc/cron.d/printbot
chmod 0644 /etc/cron.d/printbot

# Start cron in foreground
exec cron -f

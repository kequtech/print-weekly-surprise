#!/bin/sh
set -e

# Apply timezone
ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
echo "$TZ" > /etc/timezone

# Schedule the print job; log to /data/cron.log
echo "$CRON root /bin/sh /app/run.sh >> /data/cron.log 2>&1" > /etc/cron.d/print-weekly-surprise
chmod 0644 /etc/cron.d/print-weekly-surprise

# Start cron in foreground
exec cron -f

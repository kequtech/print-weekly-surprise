#!/bin/sh
set -e

# Ensure history directory exists on the mounted volume
mkdir -p /data/history

# Run main script with absolute python path (cron-safe)
exec /usr/local/bin/python /app/print-weekly-surprise.py

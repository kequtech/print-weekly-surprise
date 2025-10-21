#!/bin/sh
set -e

# Ensure history directory exists
mkdir -p /data/history

# Run main script
exec python /data/print-weekly-surprise.py

# kequc/print-weekly-surprise
# Print a random comic, image, and quote once per week using a CUPS printer.
# Prevent print head clogging.

FROM python:3.12-slim

# --- Default environment variables ---
ENV PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    TZ=Etc/UTC \
    PAPER=A4 \
    PRINT=1 \
    CRON="30 9 * * MON" \
    QUEUE=epson-et1810 \
    CUPS_HOST=127.0.0.1:631 \
    BG_SATURATION=0.7

# --- System dependencies ---
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        cron cups-client fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# --- Working directory ---
WORKDIR /data
COPY print-weekly-surprise.py run.sh scheduler.sh ./
RUN chmod +x /data/*.sh

# --- Data persistence ---
VOLUME ["/data"]

# --- Python dependencies ---
RUN python -m pip install --no-cache-dir pillow

# --- Output directory ---
RUN mkdir -p /data/history

# --- Metadata (visible in Ugreen & Docker Hub) ---
LABEL org.opencontainers.image.title="Print Weekly Surprise" \
      org.opencontainers.image.description="Print a random comic, image, and quote once per week using a CUPS printer. Prevent print head clogging." \
      org.opencontainers.image.version="1.1.3" \
      org.opencontainers.image.authors="Nathan Lunde-Berry <contact@kequtech.com>" \
      org.opencontainers.image.url="https://hub.docker.com/r/kequc/print-weekly-surprise" \
      org.opencontainers.image.source="https://github.com/kequtech/print-weekly-surprise" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.environment="TZ=Etc/UTC,CRON=30 9 * * MON,PRINT=1,PAPER=A4,QUEUE=epson-et1810,CUPS_HOST=127.0.0.1:631,BG_SATURATION=0.7"

ENTRYPOINT ["/bin/sh", "/data/scheduler.sh"]

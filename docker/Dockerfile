FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY src ./src
COPY data ./data

# Cron job
COPY docker/cron_job /etc/cron.d/hn_etl_cron
RUN chmod 0644 /etc/cron.d/hn_etl_cron && crontab /etc/cron.d/hn_etl_cron

# Start cron in foreground
CMD ["cron", "-f"]

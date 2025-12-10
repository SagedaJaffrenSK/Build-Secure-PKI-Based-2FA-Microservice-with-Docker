FROM python:3.10-slim

WORKDIR /app

# Install cron and bash
RUN apt-get update && apt-get install -y --no-install-recommends cron bash \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app ./app
COPY cron ./cron
COPY scripts ./scripts
COPY commit.sig .
COPY student_private.pem .
COPY instructor_public.pem .

# Permissions
RUN chmod +x /scripts/entrypoint.sh || true

# Persistent directory
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8000

# Run cron + API via entrypoint
CMD ["bash", "/scripts/entrypoint.sh"]

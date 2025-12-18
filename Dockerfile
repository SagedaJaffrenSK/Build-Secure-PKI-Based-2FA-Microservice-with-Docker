FROM python:3.10-slim

WORKDIR /app

# install cron + bash
RUN apt-get update && apt-get install -y --no-install-recommends cron bash \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY app ./app
COPY cron ./cron
COPY app/scripts ./app/scripts
COPY instructor_public.pem .

# Make entrypoint executable

RUN chmod +x /scripts/entrypoint.sh || true

# Data volume for persistence
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

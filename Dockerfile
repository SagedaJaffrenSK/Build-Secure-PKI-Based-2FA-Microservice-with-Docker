FROM python:3.10-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app ./app
COPY cron ./cron
COPY scripts ./scripts
COPY commit.sig .

# Runtime directory for persistence
RUN mkdir -p /data
VOLUME ["/data"]

# Expose evaluator port
EXPOSE 8000

# Start Python API + Cron Supervisor
CMD ["python", "app/scripts/main.py"]

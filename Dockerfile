# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install cron and tzdata
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY app/ app/
COPY scripts/ scripts/
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy keys (required inside container)
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Set permissions for cron
RUN chmod 0644 /etc/cron.d/2fa-cron

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

EXPOSE 8080

# Start cron + API
CMD touch /cron/last_code.txt && cron -f & uvicorn app.main:app --host 0.0.0.0 --port 8080

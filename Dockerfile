# Simple, reproducible Django image for Kubernetes
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app \
    PORT=8000

WORKDIR $APP_HOME

# (Optional) system packages for psycopg / building deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Requirements first for better caching
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# App code
COPY . .

# Entrypoint: run migrations then gunicorn
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]

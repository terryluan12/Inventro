#!/usr/bin/env sh
set -e

# Provide defaults if not set (safe for dev)
: "${DJANGO_SETTINGS_MODULE:=inventro.settings}"
: "${PORT:=8000}"

# Database may not be ready instantly in containers; harmless here but quick retry loop is easy to add later.

# Make & apply migrations (idempotent)
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# Optional: collect static (won't fail if STATIC_ROOT not set)
python manage.py collectstatic --noinput || true

# Start app
exec gunicorn inventro.wsgi:application --bind "0.0.0.0:${PORT}" --workers 3

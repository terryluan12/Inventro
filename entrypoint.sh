#!/bin/bash
cd inventro

echo "Running makemigrations..."
python manage.py makemigrations --noinput

echo "Running makemigrations..."
python manage.py collectstatic


echo "Running migrate..."
python manage.py migrate --noinput

echo "Creating Superuser..."
python manage.py createsuperuser --noinput 

echo "Populating Database..."
cd inventory/util
python populate_database.py
cd ../..

if [[ $DEBUG == "0" ]]; then
    echo "Starting Gunicorn..."
    exec gunicorn inventro.wsgi:application --bind 0.0.0.0:8000 --workers 3
else 
    echo "Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
fi
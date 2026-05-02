#!/bin/bash

echo "Starting Server..."
python manage.py makemigrations
python manage.py migrate
python manage.py seed_urls
python manage.py collectstatic --noinput
#python manage.py runserver
gunicorn WebCrawler.wsgi:application --bind 0.0.0.0:8000
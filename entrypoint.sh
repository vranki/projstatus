#!/bin/bash
echo "Starting server"
pipenv run python3 manage.py runserver 0.0.0.0:8000
#pipenv run gunicorn drfx.wsgi:application --bind 0.0.0.0:8000


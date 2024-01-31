#!/bin/bash

# Create index and index old articles
yes | python manage.py search_index --rebuild

# Migrate to apply any new db update
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000 &

exec "$@"

sleep infinity
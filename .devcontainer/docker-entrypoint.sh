#!/bin/bash

if [ "$1" == "backend" ]; then
    # Create index and index old articles
    yes | python manage.py search_index --rebuild

    # Migrate to apply any new db update
    python manage.py makemigrations article search_indexes user
    python manage.py migrate

    # Start the server
    python manage.py runserver 0.0.0.0:8000 &
else # frontend
    # make sure the image has latest source
    yes | git pull
    # Start the server (dev)
    npm run dev
fi

exec "${@:2}"

sleep infinity
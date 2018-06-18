#!/bin/sh
apk update && apk upgrade 
apk add $(cat apk.txt)
make init-prod
python manage.py migrate
python manage.py collectstatic --noinput

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn mes-cloud.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --log-level=info \
    "$@"

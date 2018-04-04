#!/bin/sh
apk update -y
apk upgrade -y
apk add $(cat apk.txt)
pip3 install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn mes-cloud.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --log-level=info \
    "$@"

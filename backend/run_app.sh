#!/bin/sh

while ! nc -z db 5432;
    do sleep .5;
    echo "wait database";
done;
    echo "connected to the database";

python manage.py migrate;
python manage.py collectstatic --noinput;
gunicorn -w 2 -b 0:8000 foodgram.wsgi;

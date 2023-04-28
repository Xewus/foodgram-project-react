#!/bin/sh

while ! nc -z db 5432;
    do sleep .5;
    echo "wait database";
done;
    echo "connected to the database";

python backend/manage.py migrate --pythonpath .;
python backend/manage.py collectstatic --noinput --pythonpath .;
gunicorn -w 2 -b 0:8000 backend.foodgram.wsgi --preload;

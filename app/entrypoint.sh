#!/bin/sh

if [[ -z "${SECRET_KEY}" ]];  then
  export SECRET_KEY=$(python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
fi

python manage.py collectstatic --no-input -v 2

gunicorn --bind :8000 --workers 3 LandCollection.wsgi:application
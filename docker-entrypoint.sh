#!/bin/sh

set -e

# echo "Waiting for postgres..."
# while ! nc -z $DB_HOST $DB_PORT; do
#   sleep 0.1
# done
# echo "PostgreSQL started"

# Make web owner of static folders
# chown -R app:app /opt/app/static/
# chown -R app:app /var/www/static/

# Run app as web

python manage.py collectstatic --noinput
python manage.py migrate

DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput || true

# uwsgi --strict --ini /opt/app/uwsgi.ini
gunicorn django_config.wsgi:application --bind 0.0.0.0:8000 --reload
# python manage.py runserver

# exec runuser -u app "$@"

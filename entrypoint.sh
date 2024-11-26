#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python src/manage.py makemigrations
python src/manage.py migrate --no-input
python src/manage.py collectstatic --no-input
python src/manage.py compilemessages

python src/manage.py create_admin_user

exec "$@"

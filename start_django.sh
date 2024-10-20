#!/bin/sh
echo "Setting up Django"

poetry run python manage.py makemigrations
poetry run python manage.py migrate

# create superuser
poetry run python manage.py createsuperuser --username jenny --email jlo@acme.com --noinput

# wait for Neo4J: podman compose does not respect the health check
echo "Waiting for Neo4J"
sleep 20

# create demo data in Django and Neo4j
echo "Setting up demo data"
poetry run python manage.py demodata

# start Django
echo "Starting Django"
poetry run python manage.py runserver "0.0.0.0:8000"
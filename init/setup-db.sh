#!/usr/bin/env bash

# Fail if any command fails.
set -e

docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py loaddata init/organizations.json
docker-compose exec web python manage.py createsuperuser
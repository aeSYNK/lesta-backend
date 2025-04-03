#!/bin/bash

echo "Backend is being launched"

# Migrate
if [[ ${RUN_DB_MIGRATIONS} == true ]]; then
  echo "Running DATABASE migrations..."
  echo "python manage.py migrate"
  python manage.py migrate --noinput
fi


exec "$@"

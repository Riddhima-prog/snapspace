#!/usr/bin/env bash
set -o errexit
python -m pip install --upgrade pip
pip install -r requirements.txt
# Bootstrap the app's initial schema on a fresh deployment.
python manage.py makemigrations social
python manage.py migrate --noinput
python manage.py collectstatic --noinput

#!/bin/bash

source /var/app/venv/*/bin/activate && {


# log which migrations have already been applied
python library_api/manage.py showmigrations;
# migrate the rest
python library_api/manage.py migrate --noinput;
# another command to create a superuser (write your own)
}

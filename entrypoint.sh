#!/bin/sh

python3.8 /opt/api_test/df_drf/manage.py makemigrations
python3.8 /opt/api_test/df_drf/manage.py migrate

python3.8 /opt/api_test/df_drf/manage.py loaddata /opt/api_test/df_drf/df_drf/fixtures/users.json
python3.8 /opt/api_test/df_drf/manage.py loaddata /opt/api_test/df_drf/cars/fixtures/brands.json
python3.8 /opt/api_test/df_drf/manage.py loaddata /opt/api_test/df_drf/cars/fixtures/cars.json
python3.8 /opt/api_test/df_drf/manage.py loaddata /opt/api_test/df_drf/df_drf/fixtures/applications.json


#!/bin/bash
cd `dirname $0`
cd example_app
epio delete
rm .epio-app
sleep 5
epio create ihpscorecard
../deploy.sh
epio django loaddata example_data.json
epio django createsuperuser -- --username=admin --email=admin@example.org --noinput
echo -e "from django.contrib.auth import models;models.User.objects.get(username='admin').set_password('abc123');exit()" | epio django shell

#!/bin/bash
rm testing.db; 
./manage.py syncdb --noinput --settings=local_settings; 
./manage.py createsuperuser --username=admin --email=admin@example.org --noinput --settings=local_settings;
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | ./manage.py shell --settings=local_settings

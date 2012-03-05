#!/bin/bash
./manage.py flush --noinput --settings=local_settings
./manage.py reset scorecard_processor --noinput --settings=local_settings
./manage.py syncdb --noinput --settings=local_settings
./manage.py createsuperuser --username=admin --email=admin@example.org --noinput --settings=local_settings 
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | ./manage.py shell --settings=local_settings 
./manage.py loaddata ihp_results/project_data/project.json   --settings=local_settings 
./manage.py loaddata ihp_results/project_data/entities.json   --settings=local_settings 
./manage.py loaddata ihp_results/project_data/surveys.json --settings=local_settings 
./manage.py loaddata ihp_results/project_data/reports.json   --settings=local_settings 

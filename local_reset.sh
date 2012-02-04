#!/bin/bash
./manage.py flush --noinput --settings=local_settings
./manage.py syncdb --noinput --settings=local_settings
./manage.py createsuperuser --username=admin --email=admin@example.org --noinput --settings=local_settings 
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | ./manage.py shell --settings=local_settings 
./manage.py loaddata ihp_results/example_data.json --settings=local_settings 
#echo -e "from scorecard_processor.models import ReportRun;r=ReportRun.objects.get(id=1);r.source_data={'data_series':5};r.save();exit()" | ./manage.py shell --settings=local_settings

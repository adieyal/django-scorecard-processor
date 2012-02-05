#!/bin/bash
./manage.py flush --noinput --settings=local_settings
./manage.py reset scorecard_processor --noinput --settings=local_settings
./manage.py syncdb --noinput --settings=local_settings
./manage.py createsuperuser --username=admin --email=admin@example.org --noinput --settings=local_settings 
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | ./manage.py shell --settings=local_settings 
./manage.py loaddata ihp_results/example_data.json --settings=local_settings 
echo -e "from django.contrib.auth import models;from scorecard_processor.models import Entity;u=models.User.objects.create(username='radbrad182@gmail.com', email='radbrad182@gmail.com', first_name='Bradley', last_name='Whittington');u.set_password('abc123');u.entity_set.add(Entity.objects.get(abbreviation='WHO'));u.save();exit()" | ./manage.py shell --settings=local_settings 
#echo -e "from scorecard_processor.models import ReportRun;r=ReportRun.objects.get(id=1);r.source_data={'data_series':5};r.save();exit()" | ./manage.py shell --settings=local_settings

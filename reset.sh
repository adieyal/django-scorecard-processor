#!/bin/bash
cd `dirname $0`
cd ihp
epio django flush --noinput
../deploy.sh
epio django loaddata ihp_results/example_data.json
epio django createsuperuser -- --username=admin --email=admin@example.org --noinput
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | epio django shell
#echo -e "from scorecard_processor.models import ReportRun;r=ReportRun.objects.get(id=1);r.source_data={'data_series':5};r.save();exit()" | epio django shell

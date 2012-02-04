#!/bin/bash
cd `dirname $0`
cd ihp
epio django flush -a ihp_prod
../deploy_ihp.sh
epio django loaddata ihp_results/example_data.json -a ihp_prod
epio django createsuperuser -a ihp_prod -- --username=admin --email=admin@example.org --noinput 
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | epio django shell -a ihp_prod
echo -e "from django.contrib.sites import models;s=models.Site.objects.get_current();s.name='IHP+Results';s.domain='survey2012.ihpresults.net';s.save();exit()" | epio django shell -a ihp_prod
#echo -e "from scorecard_processor.models import ReportRun;r=ReportRun.objects.get(id=1);r.source_data={'data_series':5};r.save();exit()" | epio django shell

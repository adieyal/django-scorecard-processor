#!/bin/bash
cd `dirname $0`
cd ihp
epio django flush -a ihp_prod -- --noinput
epio django reset scorecard_processor -a ihp_prod -- --noinput
epio django createsuperuser -a ihp_prod -- --username=admin --email=admin@example.org --noinput 
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | epio django shell -a ihp_prod
echo -e "from django.contrib.sites import models;s=models.Site.objects.get_current();s.name='IHP+Results';s.domain='survey2012.ihpresults.net';s.save();exit()" | epio django shell -a ihp_prod
../deploy_ihp.sh
epio django loaddata ihp_results/example_data.json -a ihp_prod
echo -e "from django.contrib.auth import models;from scorecard_processor.models import Entity;u=models.User.objects.create(username='radbrad182@gmail.com', email='radbrad182@gmail.com', first_name='Bradley', last_name='Whittington');u.set_password('abc123');u.entity_set.add(Entity.objects.get(abbreviation='WHO'));u.save();exit()" | epio django shell -a ihp_prod
echo -e "from django.contrib.auth import models;from scorecard_processor.models import Entity;u=models.User.objects.create(username='james@human-scale.net', email='james@human-scale.net', first_name='James', last_name='Fairfax');u.set_password('abc123');u.entity_set.add(Entity.objects.get(abbreviation='WHO'));u.save();exit()" | epio django shell -a ihp_prod
#echo -e "from scorecard_processor.models import ReportRun;r=ReportRun.objects.get(id=1);r.source_data={'data_series':5};r.save();exit()" | epio django shell

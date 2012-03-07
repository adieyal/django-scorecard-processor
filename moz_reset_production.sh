#!/bin/bash
cd `dirname $0`
cd moz
#epio django flush  -- --noinput
#epio django reset scorecard_processor -- --noinput
epio django createsuperuser  -- --username=admin --email=admin@example.org --noinput 
echo -e "from django.contrib.auth import models;u=models.User.objects.get(username='admin');u.set_password('abc123');u.save();exit()" | epio django shell 
echo -e "from django.contrib.sites import models;s=models.Site.objects.get_current();s.name='Mozambique';s.domain='moz2012.ihpresults.net';s.save();exit()" | epio django shell 
../moz_deploy.sh
epio django loaddata moz_results/project_data/project.json
epio django loaddata moz_results/project_data/entities.json
epio django loaddata moz_results/project_data/surveys.json
epio django loaddata moz_results/project_data/reports.json

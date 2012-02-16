#!/bin/bash
echo -e "from django.contrib.auth import models;[u.entity_set.clear() for u in models.User.objects.all()];exit()" | ./manage.py shell --settings=local_settings 
./manage.py dumpdata `for i in Project DataSeries DataSeriesGroup;do echo -n "scorecard_processor.$i "; done` --settings=local_settings --indent=2 > ihp_results/project_data/project.json
./manage.py dumpdata `for i in Entity EntityType;do echo -n "scorecard_processor.$i "; done` --settings=local_settings --indent=2 > ihp_results/project_data/entities.json
./manage.py dumpdata `for i in Survey Question QuestionGroup ImportMap ImportFieldMap ResponseOverride SurveyTranslation QuestionTranslation QuestionGroupTranslation;do echo -n "scorecard_processor.$i "; done` --settings=local_settings --indent=2 > ihp_results/project_data/surveys.json
./manage.py dumpdata `for i in Scorecard Operation OperationArgument ReportRun;do echo -n "scorecard_processor.$i "; done` --settings=local_settings --indent=2 > ihp_results/project_data/reports.json

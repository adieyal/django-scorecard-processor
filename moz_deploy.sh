#!/bin/bash
PROJECT=moz
cd `dirname $0`
rm -rf /tmp/$PROJECT/
cp -R $PROJECT /tmp/
rm /tmp/$PROJECT/scorecard_processor
rm /tmp/$PROJECT/*db
cp -R django-scorecard-processor/scorecard_processor /tmp/$PROJECT/
cd /tmp/$PROJECT/
epio upload 
epio django sync_permissions 
epio django syncdb  -- --noinput
epio django migrate 
cd -
rm -rf /tmp/$PROJECT/

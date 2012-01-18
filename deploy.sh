#!/bin/bash
cd `dirname $0`
rm -rf /tmp/ihp/
cp -R ihp /tmp/
rm /tmp/ihp/scorecard_processor
rm /tmp/ihp/*db
cp -R django-scorecard-processor/scorecard_processor /tmp/ihp/
cd /tmp/ihp/
epio upload
curl http://ihpscorecard.ep.io > /dev/null &
epio django syncdb -- --noinput
epio django migrate
cd -
rm -rf /tmp/ihp/

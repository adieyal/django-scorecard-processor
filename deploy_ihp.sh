#!/bin/bash
cd `dirname $0`
rm -rf /tmp/ihp/
cp -R ihp /tmp/
rm /tmp/ihp/scorecard_processor
rm /tmp/ihp/*db
cp -R django-scorecard-processor/scorecard_processor /tmp/ihp/
cd /tmp/ihp/
epio upload -a ihp_prod
curl http://ihp_prod.ep.io > /dev/null &
epio django syncdb -a ihp_prod -- --noinput
epio django migrate -a ihp_prod
cd -
rm -rf /tmp/ihp/

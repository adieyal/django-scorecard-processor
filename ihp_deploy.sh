#!/bin/bash
cd `dirname $0`
rm -rf /tmp/ihp/
cp -R ihp /tmp/
rm /tmp/ihp/scorecard_processor
rm /tmp/ihp/*db
cp -R django-scorecard-processor/scorecard_processor /tmp/ihp/
cd /tmp/ihp/
epio upload -a ihp_prod
(curl http://survey2012.ihpresults.net;curl http://survey2012.ihpresults.net)  > /dev/null &
epio django sync_permissions -a ihp_prod 
epio django syncdb -a ihp_prod -- --noinput
epio django migrate -a ihp_prod
cd -
rm -rf /tmp/ihp/

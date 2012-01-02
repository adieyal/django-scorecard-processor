#!/bin/bash
cd `dirname $0`
rm -rf /tmp/example_app/
cp -R example_app /tmp/
rm /tmp/example_app/scorecard_processor
rm /tmp/example_app/*db
cp -R django-scorecard-processor/scorecard_processor /tmp/example_app/
cd /tmp/example_app/
epio upload -a ihp_prod
curl http://ihp_prod.ep.io > /dev/null &
epio django syncdb -a ihp_prod -- --noinput
epio django migrate -a ihp_prod
cd -
rm -rf /tmp/example_app/

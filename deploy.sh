#!/bin/bash
cd `dirname $0`
rm -rf /tmp/example_app/
cp -R example_app /tmp/
rm /tmp/example_app/scorecard_processor
cp -R django-scorecard-processor/scorecard_processor /tmp/example_app/
cd /tmp/example_app/
epio upload
epio django syncdb
epio django migrate
cd -
rm -rf /tmp/example_app/

#!/bin/bash
cd `dirname $0`
rm -rf /tmp/example_app/
cp -R example_app /tmp/
cp -R django-scorecard-processor/scorecard_processor /tmp/example_app/
cd /tmp/example_app/
epio upload
rm -rf /tmp/example_app/

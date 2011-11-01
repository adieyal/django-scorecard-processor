#!/bin/bash
cd `dirname $0`
rm -rf /tmp/example_app/
cp -RL example_app /tmp/
cd /tmp/example_app/
epio upload
rm -rf /tmp/example_app/

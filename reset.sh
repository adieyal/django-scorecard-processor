#!/bin/bash
cd `dirname $0`
cd example_app
epio delete
rm .epio-app
epio create ihpscorecard
../deploy.sh

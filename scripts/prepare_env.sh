#!/bin/sh -ex

cd `dirname $0`
cd ..

python scripts/virtualenv.py test
. ./test/bin/activate
pip install -v --requirement `pwd`/ihp/requirements.txt
pip install epio

cd ihp/
./manage.py syncdb  --settings=local_settings
./manage.py migrate  --settings=local_settings


#./manage.py test

echo "Run source test/bin/activate"

#! /bin/bash

pip install -r reqs/test.txt

coverage run manage.py test --settings=calorie_app.settings.test

if [ $? -eq 0 ]; then
	echo "Coverage test passed"
else
	echo "Coverage test failed"
	exit 1
fi

coverage report && coverage xml
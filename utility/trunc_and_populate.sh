#!/usr/bin/env bash

echo "Truncating the database."
if [[ "$OSTYPE" == "openbsd"* ]]; then
	psql -U postgres -f utility/truncate_script.sql ctrack
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
	sudo -u postgres psql -f utility/truncate_script.sql ctrack
else
	echo "Cannot detect operating system"
fi

sleep 1

echo "Populating the database with test data."
python manage.py populate_db

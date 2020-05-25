#!/usr/bin/env bash

echo "Truncating the database."
psql -U postgres -a -f /home/lemon/code/python/ctrack/utility/truncate_script.sql ctrack

sleep 1

echo "Populating the database with test data."
python manage.py populate_db

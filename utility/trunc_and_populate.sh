#!/usr/bin/env bash

echo "Truncating the database."
sudo -u postgres psql -f utility/truncate_script.sql ctrack

sleep 1

echo "Populating the database with test data."
python manage.py populate_db

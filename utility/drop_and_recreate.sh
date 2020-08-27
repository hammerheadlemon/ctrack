#!/usr/bin/env bash

echo "Ensure this is run from project root."
echo "Dropping database..."
sudo -u postgres psql -f utility/drop_and_recreate.sql
echo "Done."


#!/usr/bin/env bash

echo "Ensure this is run from project root."
echo "Dropping database..."

if [[ "$OSTYPE" == "openbsd"* ]]; then
	#doas -u _postgresql psql -f utility/drop_and_recreate.sql
	psql -U postgres -f utility/drop_and_recreate.sql
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
	sudo -u postgres psql -f utility/drop_and_recreate.sql
else
	echo "Cannot detect operating system"
fi

echo "Done."

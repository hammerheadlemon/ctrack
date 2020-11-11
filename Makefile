SUPERUSER_NAME=mlemon
SUPERUSER_PASSWD=lemonlemon
SUPERUSER_EMAIL=bob@bob.com
DATABASE_NAME=ctrack
DATABASE_USER=postres

test:
	pytest --tb=short -v

test-fast:
	pytest -k "not test_functional" --tb=short

initialisedb: populate
	python manage.py createsuperuser

populate: migrate
	@echo "Populating new database with test data."
	python manage.py populate_db

migrate: createdb 
	@echo "Migrating."
	python manage.py migrate

createdb: dropdb
	@echo "Creating a new database."
	createdb $(DATABASE_NAME) -O postgres

dropdb:
	@echo "Dropping any existing ctrack database."
	psql -U postgres -c "DROP DATABASE IF EXISTS $(DATABASE_NAME);"

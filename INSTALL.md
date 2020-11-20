## Development installation

**CAVEATS**

THIS SYSTEM DOES NOT HANDLE CAF DATA. And it probably never will. There are
obvious security concerns with hosting sensitive aggregated data on anything
but the most secure systems.  This project currently only manages the
management data involved with NIS compliance: it is a basic CRM/CRUD
application that handles contacts, events, etc.

There is, in the background, some facility to store CAF data, but this is not
currently brought out in the user interface. Find it in the admin interface.

It does work nicely for what it is though - and it is still in development so
consider it to be very unstable. Email me at y at yulqen dot org.

---

To install `ctrack` to enable testing and development on your local machine
(Mac and Linux environment only).

You need to have `sudo` rights on the machine.

### Dependencies

* Python 3.8 or higher
* python3-venv (on Debian based distribution)
* git

I recommend SQLite or PostgreSQL for the database whilst testing. Current test
configuration uses PostgreSQL.

To install PostgreSQL on Debian-based distribution:

* `sudo apt update`
* `sudo apt install postgresql`
* `sudo apt install python3-venv`

You will probably need to start the database server with `sudo pg_ctlcluster 11 main
start`.

If you use SQLite, you will need to change the configuration in
`ctrack.config.settings.gcloud_settings`.

### Django set up

Get the code:

* `git clone https://github.com/yulqen/ctrack`
* `cd ctrack`

Create and activate a new virtual environment:

* `python3 -m venv .venv`
* `source .venv/bin/activate`

Install Django and python dependencies:

* `pip install -r requirments.txt`

Set up the ctrack database:

* `sudo -u postgres psql postgres`
* `CREATE DATABASE ctrack;`
* `ALTER ROLE postgres WITH PASSWORD 'postgres;'`
* `\q` (to quit `psql`)`

Note - never use this default username/password configuration on a production
server! This is for testing only.

Migrate:

* `python manage.py migrate`


Create a superuser:

* `python manage.py createsuperuser`

Run tests (optional, and there will be some failures):

* `pytest -k "not test_functional"`

If you want dummy data to play with:

* `python manage.py populate_db`

Run server:

* `python manage.py runserver`


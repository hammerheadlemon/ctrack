# Resetting Migrations

When you absolutely balls it up and you want to start again,  
Make sure you do the following:

You first need to remove those pesky migrations from your thing:  
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

Then you need to eradicate that old database and create a new one!  
In PostgreSQL, that's easy:  
```bash
sudo -u postgres psql
DROP DATABASE <database_name>
CREATE DATBASE <database_name>
\q
```

Now, to recreate those migrations...  
Here is what you do:

```bash
python manage.py makemigrations
python manage.py migrate
```

If `allauth` social accounts gives you problems - and it can:  
You need to except this app from your application momentarily...
Comment it out of your settings.  
Run your migrations again.

You are good, my friend.

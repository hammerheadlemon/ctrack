# Generated by Django 3.0.5 on 2020-05-25 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200524_1945'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

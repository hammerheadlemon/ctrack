# Generated by Django 3.0.5 on 2020-05-22 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_person'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_person',
            new_name='oes_user',
        ),
    ]
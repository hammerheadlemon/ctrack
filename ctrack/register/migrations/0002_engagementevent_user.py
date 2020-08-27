# Generated by Django 2.2.12 on 2020-08-27 09:40

import ctrack.register.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementevent',
            name='user',
            field=models.ForeignKey(on_delete=models.SET(ctrack.register.models.EngagementEvent.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]

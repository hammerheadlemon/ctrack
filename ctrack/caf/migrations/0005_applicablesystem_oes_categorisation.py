# Generated by Django 2.2.12 on 2020-08-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caf', '0004_auto_20200813_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicablesystem',
            name='oes_categorisation',
            field=models.CharField(choices=[('CR', 'Critical'), ('IM', 'Important')], default='CR', max_length=2),
        ),
    ]

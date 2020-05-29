# Generated by Django 2.2.12 on 2020-05-29 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0008_auto_20200529_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentreport',
            name='person_involved',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name of person reporting/detecting incident'),
        ),
    ]
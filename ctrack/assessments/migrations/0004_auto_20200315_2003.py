# Generated by Django 2.2.9 on 2020-03-15 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_auto_20200315_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafcontributingoutcome',
            name='name',
            field=models.CharField(help_text='e.g. Board Direction', max_length=100),
        ),
    ]
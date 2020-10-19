# Generated by Django 3.1.2 on 2020-10-19 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_auto_20201015_1955'),
        ('register', '0004_auto_20201017_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singledatetimeevent',
            name='participants',
            field=models.ManyToManyField(to='organisations.Person'),
        ),
        migrations.AlterField(
            model_name='singledatetimeevent',
            name='type_descriptor',
            field=models.CharField(choices=[('MEETING', 'Meeting'), ('PHONE_CALL', 'Phone Call'), ('VIDEO_CALL', 'Video Call'), ('EMAIL', 'Email'), ('NOTE', 'Note')], max_length=50, verbose_name='Event Type'),
        ),
    ]

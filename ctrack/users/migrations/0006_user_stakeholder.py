# Generated by Django 3.0.5 on 2020-05-25 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0005_auto_20200525_1502'),
        ('users', '0005_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stakeholder',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.Stakeholder'),
        ),
    ]

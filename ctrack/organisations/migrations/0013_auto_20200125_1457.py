# Generated by Django 2.2.9 on 2020-01-25 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0012_organisation_submode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='submode',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.Submode'),
        ),
    ]

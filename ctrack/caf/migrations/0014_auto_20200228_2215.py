# Generated by Django 2.2.9 on 2020-02-28 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caf', '0013_auto_20200227_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essentialservice',
            name='caf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='caf.CAF'),
        ),
    ]

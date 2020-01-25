# Generated by Django 2.2.9 on 2020-01-25 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0010_auto_20200124_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Submode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(max_length=100)),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.Mode')),
            ],
        ),
    ]

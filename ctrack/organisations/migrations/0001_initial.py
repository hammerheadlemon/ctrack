# Generated by Django 3.1.2 on 2020-10-21 15:51

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=255)),
                ('line2', models.CharField(blank=True, max_length=255)),
                ('line3', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('county', models.CharField(blank=True, max_length=100)),
                ('postcode', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=100)),
                ('other_details', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='AddressType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_involved', models.CharField(blank=True, max_length=100, verbose_name='Name of person reporting/detecting incident')),
                ('role', models.CharField(blank=True, help_text='Role of person reporting/detecting incident', max_length=100)),
                ('phone_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('internal_incident_number', models.CharField(blank=True, max_length=30)),
                ('date_time_incident_detected', models.DateTimeField(verbose_name='Date/Time incident detected')),
                ('date_time_incident_reported', models.DateTimeField(auto_now=True, verbose_name='Date/Time incident reported')),
                ('incident_type', models.CharField(choices=[('Cyber', 'Cyber'), ('Non-Cyber', 'Non-Cyber'), ('Both', 'Both'), ('Power Outage', 'Power Outage')], help_text='This can be appoximate', max_length=20)),
                ('incident_status', models.CharField(choices=[('Detected', 'Detected'), ('Suspected', 'Suspected'), ('Resolved', 'Resolved')], max_length=20)),
                ('incident_stage', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Ended', 'Ended'), ('Ongoing but managed', 'Ongoing but managed')], max_length=20)),
                ('summary', models.TextField(help_text='Please provide a summary of your understanding of the incident, including any impact to services and/or users.')),
                ('mitigations', models.TextField(help_text='What investigations and/or mitigations have you or a third party performed or plan to perform?', verbose_name='Investigations or mitigations')),
                ('others_informed', models.TextField(help_text='Who else has been informed about this incident?(CSIRT, NCSC, NCA, etc)', verbose_name='Others parties informed')),
                ('next_steps', models.TextField(help_text='What are your planned next steps?', verbose_name='Planned next steps')),
                ('dft_handle_status', models.CharField(choices=[('QUEUED', 'QUEUED'), ('REVIEWING', 'REVIEWING'), ('WAITING', 'WAITING'), ('COMPLETED', 'COMPLETED')], default='QUEUED', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name'])),
                ('oes', models.BooleanField(default=True)),
                ('designation_type', models.IntegerField(choices=[(1, 'Automatic'), (2, 'Reserve Power'), (3, 'NA')], default=1)),
                ('registered_company_name', models.CharField(blank=True, max_length=255)),
                ('registered_company_number', models.CharField(blank=True, max_length=100)),
                ('date_updated', models.DateField(auto_now=True)),
                ('comments', models.TextField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_nis_contact', models.BooleanField(default=False, verbose_name='Primary NIS contact')),
                ('voluntary_point_of_contact', models.BooleanField(default=False)),
                ('has_egress', models.BooleanField(default=False, verbose_name='Has Egress')),
                ('title', models.IntegerField(choices=[(1, 'Mr'), (2, 'Mrs'), (3, 'Miss'), (4, 'Ms'), (5, 'Dr.'), (6, 'Professor'), (7, 'The Rt Hon.'), (8, 'Lord'), (9, 'Lady')], default=1)),
                ('job_title', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('secondary_email', models.EmailField(blank=True, max_length=254)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('landline', models.CharField(blank=True, max_length=20)),
                ('date_updated', models.DateField(auto_now=True)),
                ('clearance', models.IntegerField(choices=[(1, 'NA'), (2, 'BPSS'), (3, 'CTC'), (4, 'SC'), (5, 'DV'), (6, 'Other')], default=1)),
                ('clearance_sponsor', models.CharField(blank=True, max_length=100)),
                ('clearance_start_date', models.DateField(blank=True, null=True)),
                ('clearance_last_checked', models.DateField(blank=True, null=True)),
                ('clearance_expiry', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('date_ended', models.DateField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, max_length=1000)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation')),
                ('predecessor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_person', to='organisations.person')),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Submode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(max_length=100)),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.mode')),
            ],
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ManyToManyField(to='organisations.Role'),
        ),
    ]

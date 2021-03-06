# Generated by Django 3.1.2 on 2020-10-21 15:51

import ctrack.register.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisations', '0002_auto_20201021_1551'),
        ('register', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('caf', '0002_auto_20201021_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='singledatetimeevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noteevent',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation'),
        ),
        migrations.AddField(
            model_name='noteevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='engagementevent',
            name='participants',
            field=models.ManyToManyField(blank=True, to='organisations.Person'),
        ),
        migrations.AddField(
            model_name='engagementevent',
            name='related_caf',
            field=models.ForeignKey(blank=True, help_text='If the event relates to a CAF, refer to it here.', null=True, on_delete=django.db.models.deletion.CASCADE, to='caf.caf'),
        ),
        migrations.AddField(
            model_name='engagementevent',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.engagementtype'),
        ),
        migrations.AddField(
            model_name='engagementevent',
            name='user',
            field=models.ForeignKey(on_delete=models.SET(ctrack.register.models.EngagementEvent.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='caftwindateevent',
            name='related_caf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caf.caf'),
        ),
        migrations.AddField(
            model_name='caftwindateevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cafsingledateevent',
            name='related_caf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caf.caf'),
        ),
        migrations.AddField(
            model_name='cafsingledateevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='caftwindateevent',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, end_date__lt=django.db.models.expressions.F('date')), name='register_caftwindateevent_cannot_precede_start_date'),
        ),
        migrations.AddConstraint(
            model_name='cafsingledateevent',
            constraint=models.UniqueConstraint(condition=models.Q(_negated=True, type_descriptor='CAF_EMAILED_ROSA'), fields=('date', 'type_descriptor'), name='unique_caf_for_date'),
        ),
    ]

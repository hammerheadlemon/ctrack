# Generated by Django 2.2.9 on 2020-04-03 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0005_auto_20200317_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafselfassessmentoutcomescore',
            name='baseline_assessment_score',
            field=models.CharField(choices=[('Achieved', 'Achieved'), ('Partially Achieved', 'Partially Achieved'), ('Not Achieved', 'Not Achieved')], help_text='Choose an assessment score', max_length=20, verbose_name='Baseline Score'),
        ),
        migrations.AlterField(
            model_name='cafselfassessmentoutcomescore',
            name='caf_contributing_outcome',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.CAFContributingOutcome', verbose_name='CAF Contributing Outcome'),
        ),
        migrations.AlterField(
            model_name='cafselfassessmentoutcomescore',
            name='caf_self_assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.CAFSelfAssessment', verbose_name='CAF Self Assessment'),
        ),
        migrations.AlterField(
            model_name='cafselfassessmentoutcomescore',
            name='self_assessment_score',
            field=models.CharField(choices=[('Achieved', 'Achieved'), ('Partially Achieved', 'Partially Achieved'), ('Not Achieved', 'Not Achieved')], help_text='Choose an assessment score', max_length=20, verbose_name='Self Assessment Score'),
        ),
    ]

# Generated by Django 2.2.10 on 2020-04-03 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0013_auto_20200329_0551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='country_code',
        ),
        migrations.AddField(
            model_name='organization',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_country', to='workflow.Country', verbose_name='Country Code'),
        ),
        migrations.AlterField(
            model_name='historicalprojectagreement',
            name='project_status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='workflow.ProjectStatus', verbose_name='Project Status'),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflow.ProjectStatus', verbose_name='Project Status'),
        ),
    ]

# Generated by Django 2.2.10 on 2020-02-21 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_office_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundcode',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflow.Organization'),
        ),
    ]

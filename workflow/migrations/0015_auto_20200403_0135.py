# Generated by Django 2.2.10 on 2020-04-03 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0014_auto_20200403_0134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='code',
            new_name='country_code',
        ),
    ]

# Generated by Django 5.1.6 on 2025-04-14 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Case', '0004_alter_case_case_title'),
        ('userauths', '0016_citizen_user_recent_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='investigator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userauths.investigator'),
        ),
    ]

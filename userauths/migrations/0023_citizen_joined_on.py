# Generated by Django 5.2 on 2025-04-30 03:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0022_alter_citizen_recent_photo_upload_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizen',
            name='joined_on',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

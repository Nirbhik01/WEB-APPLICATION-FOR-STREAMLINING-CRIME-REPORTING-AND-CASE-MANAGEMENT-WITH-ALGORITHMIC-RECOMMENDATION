# Generated by Django 5.1.6 on 2025-02-24 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0010_alter_citizen_citizen_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizen',
            name='user_type',
            field=models.CharField(default='Citizen', max_length=15),
        ),
        migrations.AddField(
            model_name='investigator',
            name='user_type',
            field=models.CharField(default='Investigator', max_length=15),
        ),
    ]

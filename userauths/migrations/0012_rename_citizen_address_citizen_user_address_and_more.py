# Generated by Django 5.1.6 on 2025-04-11 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_citizen_user_type_investigator_user_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_address',
            new_name='user_address',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_email',
            new_name='user_email',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_id',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_name',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_password',
            new_name='user_password',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_phone_number',
            new_name='user_phone_number',
        ),
        migrations.RenameField(
            model_name='citizen',
            old_name='citizen_profile_picture',
            new_name='user_profile_picture',
        ),
        migrations.RenameField(
            model_name='investigator',
            old_name='investigator_address',
            new_name='user_address',
        ),
        migrations.RenameField(
            model_name='investigator',
            old_name='investigator_email',
            new_name='user_email',
        ),
        migrations.RenameField(
            model_name='investigator',
            old_name='investigator_id',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='investigator',
            old_name='investigator_name',
            new_name='user_name',
        ),
        migrations.RenameField(
            model_name='investigator',
            old_name='investigator_password',
            new_name='user_password',
        ),
        migrations.RenameField(
            model_name='investigator',
            old_name='investigator_phone_number',
            new_name='user_phone_number',
        ),
    ]

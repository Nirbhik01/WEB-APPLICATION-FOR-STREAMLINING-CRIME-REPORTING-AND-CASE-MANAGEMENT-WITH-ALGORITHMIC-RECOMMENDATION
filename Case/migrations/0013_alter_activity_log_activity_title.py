# Generated by Django 5.2 on 2025-05-02 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Case', '0012_remove_activity_log_activity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity_log',
            name='activity_title',
            field=models.CharField(default=None, max_length=500),
        ),
    ]

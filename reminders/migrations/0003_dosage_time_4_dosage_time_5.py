# Generated by Django 5.1.1 on 2024-10-01 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0002_remove_dosage_time_to_take_dosage_number_of_times_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosage',
            name='time_4',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dosage',
            name='time_5',
            field=models.TimeField(blank=True, null=True),
        ),
    ]

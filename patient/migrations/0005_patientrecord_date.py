# Generated by Django 4.2.11 on 2024-04-14 21:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_patient_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientrecord',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

# Generated by Django 4.2.11 on 2024-04-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_patient_grandname'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientrecord',
            name='Recommandation',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.11 on 2024-04-17 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_myuser_email_myuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurse',
            name='Adreess',
            field=models.CharField(default='Addis Abeba,boyle adebabay geba below', max_length=200),
        ),
    ]

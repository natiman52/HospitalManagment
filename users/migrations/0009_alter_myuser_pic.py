# Generated by Django 4.2.11 on 2024-04-18 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_nurse_adreess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='pic',
            field=models.ImageField(default='defaults/male.jpg', upload_to='defaults/'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-23 06:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_phones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetmodel',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 6, 54, 27, 793379)),
        ),
    ]
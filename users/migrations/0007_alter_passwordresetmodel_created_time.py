# Generated by Django 5.0.6 on 2024-05-23 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_passwordresetmodel_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetmodel',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 9, 30, 34, 946780)),
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-23 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_passwordresetmodel_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 11, 50, 56, 693733)),
        ),
        migrations.AlterField(
            model_name='passwordresetmodel',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 23, 11, 50, 56, 695604)),
        ),
    ]

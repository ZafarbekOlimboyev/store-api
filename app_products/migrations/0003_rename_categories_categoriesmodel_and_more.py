# Generated by Django 5.0.6 on 2024-05-23 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0002_categories_alter_productsmodel_category_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='CategoriesModel',
        ),
        migrations.AlterField(
            model_name='proimagemodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_products.productsmodel'),
        ),
    ]

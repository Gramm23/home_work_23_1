# Generated by Django 4.2.8 on 2023-12-26 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Модератор'),
        ),
    ]

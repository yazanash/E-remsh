# Generated by Django 5.1.6 on 2025-03-11 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_product_colors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productitems',
            old_name='color_code',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='productitems',
            old_name='size_label',
            new_name='size',
        ),
    ]

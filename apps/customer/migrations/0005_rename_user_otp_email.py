# Generated by Django 5.1.6 on 2025-02-20 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_otp_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='user',
            new_name='email',
        ),
    ]

# Generated by Django 5.2.1 on 2025-05-21 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_income_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='transaction_data',
            old_name='user_id',
            new_name='user',
        ),
    ]

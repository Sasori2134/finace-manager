# Generated by Django 5.2.1 on 2025-05-21 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_user_id_income_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='transaction_data',
            old_name='user',
            new_name='user_id',
        ),
    ]

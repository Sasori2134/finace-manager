# Generated by Django 5.2.1 on 2025-05-21 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_rename_user_income_user_id_and_more'),
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

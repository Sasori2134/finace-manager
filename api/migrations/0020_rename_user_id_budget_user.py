# Generated by Django 5.2.1 on 2025-05-27 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_budget_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='user_id',
            new_name='user',
        ),
    ]

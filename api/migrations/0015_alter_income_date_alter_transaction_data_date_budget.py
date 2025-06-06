# Generated by Django 5.2.1 on 2025-05-23 10:08

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_rename_user_income_user_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(default=datetime.date(2025, 5, 23)),
        ),
        migrations.AlterField(
            model_name='transaction_data',
            name='date',
            field=models.DateField(default=datetime.date(2025, 5, 23)),
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.PositiveIntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

from django.db import models
from django.utils import timezone

# Create your models here.

class Transaction_data(models.Model):
    user_id = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now().date())
    category = models.CharField(max_length=100)
    itemname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7,decimal_places=2)

class Income(models.Model):
    user_id = models.PositiveIntegerField()
    income = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now().date())


    
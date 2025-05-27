from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Transaction_data(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    date = models.DateField(default = timezone.now().date())
    category = models.CharField(max_length = 100)
    itemname = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits = 7,decimal_places=2)

class Income(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    income = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now().date())
    
#shecvale es user_id rom iyos primary key momavalshi
class Budget(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits = 7, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now().date())
    
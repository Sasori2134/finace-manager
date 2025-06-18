from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
def get_date():
    return timezone.now().date()
class Transaction_data(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE, blank=True)
    date = models.DateField(default = get_date)
    category = models.CharField(max_length = 100, blank=True)
    itemname = models.CharField(max_length = 200, blank=True)
    price = models.DecimalField(max_digits = 7,decimal_places=2)
    transaction_type = models.CharField(max_length=8)
    

class Budget(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    budget = models.DecimalField(max_digits = 7, decimal_places=2, blank=True)
    category = models.CharField(max_length=50, blank=True)
    date = models.DateField(default=get_date)

class RecurringBills(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    category = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    date = models.PositiveIntegerField()
    itemname = models.CharField(max_length=14,default='recurring_bill')
    transaction_type = models.CharField(max_length=7,default='expense')
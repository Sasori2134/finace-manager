from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Transaction_data)
admin.site.register(models.Income)
admin.site.register(models.Budget)
admin.site.register(models.RecurringBills)

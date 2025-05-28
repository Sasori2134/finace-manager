from django.urls import path
from . import views


urlpatterns = [
    path('add_transaction', views.TransactiondataCreateApiView.as_view(), name = 'add_transaction'),
    path('delete_transaction/<int:pk>', views.TransactiondataDeleteApiView.as_view(), name = 'delete_transaction'),
    path('average_max/<int:user_id>', views.average_max, name = 'average_max'),
    path('expenses/<int:user_id>', views.filtering_expenses, name = 'expenses'),
    path('sum_of_expenses/<int:user_id>', views.sum_of_expenses, name = 'sum_of_values'),
    path('add_income', views.AddIncomeCreateApiView.as_view(), name = 'add_income'),
    path('delete_income<int:pk>', views.IncomeDestroyApiView.as_view(), name = 'delete_income'),
    path('balance/<int:user_id>', views.balance, name = 'balance'),
    path('register', views.register, name ='register'),
    path('login', views.login, name ='login'),
    path('last_30_days/<int:user_id>', views.last_30_days, name = 'last_30_days'),
    path('add_budget', views.BudgetCreateApiView.as_view(), name = 'add_budget'),
    path('delete_budget', views.BudgetDestroyApiView.as_view(), name = 'delete_budget'),
    path('get_budget/<int:user_id>', views.get_budget, name = 'check_budget'),
    path('recurring_bills', views.RecurringBillsCreateApiView.as_view(), name = 'recurring_bills'),
    path('delete_recurring_bills/<int:pk>', views.RecurringBillsDestroyApiView.as_view(), name = 'delete_recurring_bills')
]
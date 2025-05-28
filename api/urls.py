from django.urls import path
from . import views


urlpatterns = [
    path('add_data',views.TransactiondataCreateApiView.as_view(),name = 'add_data'),
    path('average_max/<int:user_id>',views.average_max,name = 'average_max'),
    path('expenses/<int:user_id>',views.filtering_expenses,name = 'expenses'),
    path('sum_of_expenses/<int:user_id>',views.sum_of_expenses,name = 'sum_of_values'),
    path('add_income',views.AddIncomeCreateApiView.as_view(),name = 'add_income'),
    path('balance/<int:user_id>',views.balance,name = 'balance'),
    path('delete_transaction/<int:pk>',views.TransactiondataDeleteApiView.as_view(),name = 'delete_transaction'),
    path('register',views.register,name ='register'),
    path('login',views.login,name ='login'),
    path('last_30_days/<int:user_id>',views.last_30_days,name = 'last_30_days'),
    path('add_budget',views.BudgetCreateApiView.as_view(),name = 'add_budget'),
    path('get_budget/<int:user_id>',views.get_budget,name = 'check_budget')
]
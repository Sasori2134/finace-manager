from django.urls import path
from . import views


urlpatterns = [
    path('add_data',views.TransactiondataCreateApiView.as_view(),name = 'add_data'),
    path('average_max/<int:user_id>',views.average_max,name = 'average_max'),
    path('expenses/<int:user_id>',views.filtering_expenses,name = 'expenses'),
    path('sum_of_values/<int:user_id>',views.sum_of_values,name = 'sum_of_values'),
    path('add_income',views.AddIncomeCreateApiView.as_view(),name = 'add_income'),
    path('balance/<int:user_id>',views.balance,name = 'balance'),
    path('deletetransaction/<int:pk>',views.TransactiondataDeleteApiView.as_view(),name = 'deletetransaction'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login')
]
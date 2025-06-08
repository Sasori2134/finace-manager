from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('add_transaction', views.TransactiondataCreateApiView.as_view(), name = 'add_transaction'),
    path('delete_transaction/<int:pk>', views.TransactiondataDeleteApiView.as_view(), name = 'delete_transaction'),
    path('monthly_average/<int:user_id>', views.monthly_average, name = 'monthly_average'),
    path('expenses/<int:user_id>', views.filtering_expenses, name = 'expenses'),
    path('sum_of_transactions/<int:user_id>', views.sum_of_transactions, name = 'sum_of_transactions'),
    path('total_balance_income_expenses', views.total_balance_income_expenses, name = 'total_balance_income_expenses'),
    path('register', views.register, name ='register'),
    path('add_budget', views.BudgetCreateApiView.as_view(), name = 'add_budget'),
    path('delete_budget', views.BudgetDestroyApiView.as_view(), name = 'delete_budget'),
    path('get_budget/<int:user_id>', views.get_budget, name = 'check_budget'),
    path('recurring_bills', views.RecurringBillsCreateApiView.as_view(), name = 'recurring_bills'),
    path('delete_recurring_bills/<int:pk>', views.RecurringBillsDestroyApiView.as_view(), name = 'delete_recurring_bills'),
    path('recent_transactions/<int:user_id>', views.recent_transactions, name='recent_transactions'),
    path('average_total_income_expenses_analytics/<int:user_id>', views.average_total_income_expenses_analytics, name='average_total_income_expenses_analytics'),
    path('data_for_piechart_analytics/<int:user_id>',views.data_for_piechart_analytics,name = "data_for_piechart_analytics"),
    path('data_for_piechart_total/<int:user_id>',views.data_for_piechart_total, name = 'data_for_piechart_total'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
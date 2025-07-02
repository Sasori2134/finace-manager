from django.urls import path
from . import views, dashboard_views, analytics_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('add_transaction', views.TransactiondataCreateApiView.as_view(), name = 'add_transaction'),
    path('delete_transaction/<int:pk>', views.TransactiondataDestroyApiView.as_view(), name = 'delete_transaction'),
    path('expenses', views.filtering_expenses, name = 'expenses'),
    path('register', views.register, name ='register'),
    path('add_budget', views.BudgetCreateApiView.as_view(), name = 'add_budget'),
    path('delete_budget/<int:pk>', views.BudgetDestroyApiView.as_view(), name = 'delete_budget'),
    path('get_budget', views.get_budget, name = 'check_budget'),
    path('recurring_bills', views.RecurringBillsCreateApiView.as_view(), name = 'recurring_bills'),
    path('delete_recurring_bills/<int:pk>', views.RecurringBillsDestroyApiView.as_view(), name = 'delete_recurring_bills'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/log_out', views.log_out, name = 'log_out'),
    path('dashboard/monthly_average', dashboard_views.monthly_average, name='monthly_average'),
    path('dashboard/monthly_data', dashboard_views.monthly_data, name='monthly_data'),
    path('dashboard/total_stats', dashboard_views.total_stats, name='total_stats'),
    path('dashboard/recent_transactions', dashboard_views.recent_transactions, name='recent_transactions'),
    path('dashboard/data_for_piechart_total', dashboard_views.data_for_piechart_total, name='data_for_piechart_total'),
    path('analytics/analytics_data', analytics_views.analytics_data, name='analytics_data'),
    path('analytics/analytics_stats', analytics_views.analytics_stats, name='analytics_stats'),
    path('analytics/data_for_piechart_analytics', analytics_views.data_for_piechart_analytics, name='data_for_piechart_analytics')

]
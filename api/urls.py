from django.urls import path
from . import views
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
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('analytics_page', views.analytics_page, name = 'analytics_page')
]
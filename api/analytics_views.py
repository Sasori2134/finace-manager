from .models import Transaction_data
from django.db.models import Avg, Sum
from django.db.models.functions import ExtractYear
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def analytics_data(request):
    days = int(request.query_params.get('days', 30))
    grouped_by_day_expense = Transaction_data.objects.annotate(year = ExtractYear('date')).filter(user_id=request.user, transaction_type='expense',year = timezone.now().year, date__range = (timezone.now().date() - timedelta(days=days-1),timezone.now().date())).values('date').annotate(daily_sum = Sum('price')).order_by('date')
    grouped_by_day_income = Transaction_data.objects.annotate(year = ExtractYear('date')).filter(user_id=request.user, transaction_type='income',year = timezone.now().year, date__range = (timezone.now().date() - timedelta(days=days-1),timezone.now().date())).values('date').annotate(daily_sum = Sum('price')).order_by('date')
    start_date = datetime.now().date() - timedelta(days=days)
    expense_dates = {((start_date + timedelta(days=i)).strftime('%b-%d')) : 0 for i in range(1,days+1)}
    income_dates = expense_dates.copy()
    for i in grouped_by_day_expense:
        expense_dates[i['date'].strftime('%b-%d')] = i['daily_sum']
    for i in grouped_by_day_income:
        income_dates[i['date'].strftime('%b-%d')] = i['daily_sum']
    return Response({'daily_expense' : expense_dates,'daily_income' : income_dates})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def analytics_stats(request):
    days = int(request.query_params.get('days',30))
    income_average = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='income').aggregate(income_average = Avg('price'))['income_average']
    expense_average = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='expense').aggregate(expense_average = Avg('price'))['expense_average']
    total_income = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='income').aggregate(total_income= Sum('price'))['total_income']
    total_expense = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='expense').aggregate(total_expense = Sum('price'))['total_expense']
    return Response({'income_average': round(income_average,2), 'expense_average' : round(expense_average,2), 'total_income' : round(total_income,2), 'total_expense' : round(total_expense,2)})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def data_for_piechart_analytics(request):
    days = int(request.query_params.get('days', 30))
    grouped_by_category = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days=days), transaction_type='expense').values('category').annotate(stats = Sum('price'))
    return Response(grouped_by_category)
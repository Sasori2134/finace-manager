from practice_project.serializers import ItemSerializer
from .models import Transaction_data
from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth, ExtractYear, ExtractMonth
from django.utils import timezone


def monthly_average(request):
    expense_average = Transaction_data.objects.annotate(month = TruncMonth('date')).filter(user_id = request.user, transaction_type='expense').values('month').annotate(monthly_total = Sum('price')).aggregate(avg = Avg('monthly_total'))
    Income_average = Transaction_data.objects.annotate(month = TruncMonth('date')).filter(user_id = request.user, transaction_type='income').values('month').annotate(monthly_total = Sum('price')).aggregate(avg = Avg('monthly_total'))
    if expense_average['avg'] is None:
        expense_average['avg'] = 0
    if Income_average['avg'] is None:
        Income_average['avg'] = 0
    expense_mean, income_mean = round(expense_average['avg'],2),round(Income_average['avg'],2)
    return {'expense_average': expense_mean, 'income_average' : income_mean}


def sum_of_transactions(request):
    grouped_by_month_expense = Transaction_data.objects.annotate(year = ExtractYear('date'),month = ExtractMonth('date')).filter(user_id=request.user, transaction_type='expense',year = timezone.now().year).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    grouped_by_month_income = Transaction_data.objects.annotate(year = ExtractYear('date'), month = ExtractMonth('date')).filter(user_id=request.user, transaction_type='income',year = timezone.now().year).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    months_expenses = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    months_income = months_expenses.copy()
    for i in grouped_by_month_income:
        months_income[i['month']] = i['monthly_sum']
    for i in grouped_by_month_expense:
        months_expenses[i['month']] = i['monthly_sum']
    return {'monthly_expense' : months_expenses,'monthly_income' : months_income}


def total_balance_income_expenses(request):
    expenses = Transaction_data.objects.filter(user_id=request.user, transaction_type='expense').aggregate(price = Sum('price'))
    income = Transaction_data.objects.filter(user_id=request.user, transaction_type='income').aggregate(income = Sum('price'))
    if expenses['price'] is None:
        expenses['price'] = 0
    if income['income'] is None:
        income['income'] = 0
    balance = round(income['income'] - expenses['price'],2)
    return {'balance': balance, 'total_income' : income['income'], 'total_expense' : expenses['price']}


def recent_transactions(request):
    transactions = ItemSerializer(Transaction_data.objects.filter(user_id=request.user).order_by('-date')[:5], many=True)
    return transactions.data


def data_for_piechart_total(request):
    grouped_by_category = Transaction_data.objects.filter(user_id=request.user, transaction_type='expense').values('category').annotate(stats = Sum('price'))
    return grouped_by_category
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from practice_project.serializers import ItemSerializer, FilteredExpansesSerializer, FilteredExpansesInputSerializer, BudgetSerializer, SecondaryBudgetSerializer, RecurringBillsSerializer, RegisterInputSerializer
from rest_framework.response import Response
from .models import Transaction_data, Budget, RecurringBills
from django.db.models import Avg, Max, Sum
from django.db.models.functions import TruncMonth,TruncYear, TruncDay, ExtractYear, ExtractMonth, ExtractDay
from rest_framework import generics, permissions, authentication
from django.contrib.auth.models import User, auth
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.utils import IntegrityError


# Create your views here.
# unda gavaketo tavidan dzaan hardcoded ari
def recurring_bills_function(user):
    recurring_bills = RecurringBillsSerializer(RecurringBills.objects.filter(user_id=user), many=True)
    for i in recurring_bills.data:
        transaction_data = ItemSerializer(Transaction_data.objects.filter(user_id=user, category=i['category'],itemname='recurring_bill',transaction_type='expense').order_by('-date'), many = True)
        if transaction_data.data:
            date = datetime.strptime(transaction_data.data[0]['date'],'%Y-%m-%d').strftime('%Y-%m')
            if timezone.now().date().day >= i['date'] and date != timezone.now().date().strftime('%Y-%m'):
                i['date'] = timezone.now().date()
                serialized_data = ItemSerializer(data = i, context = {'user' : user})
                if serialized_data.is_valid():
                    serialized_data.save()
        else:
            if timezone.now().date().day >= i['date']:
                i['date'] = timezone.now().date()
                serialized_data = ItemSerializer(data = i, context = {'user' : user})
                if serialized_data.is_valid():
                    serialized_data.save()


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard(request):
    recurring_bills_function(request.user)
    return Response({
        'stats' : total_balance_income_expenses(request),
        'recent_transactions' : recent_transactions(request),
        'monthly_chart' : sum_of_transactions(request),
        'monthly_average' : monthly_average(request),
        'data_for_piechart' : data_for_piechart_total(request)
        })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def analytics_page(request):
    try:
        return Response({
        'stats' : average_total_income_expenses_analytics(request),
        'piechart' : data_for_piechart_analytics(request),
        'chart' : sum_of_transactions_analytics(request)
        })
    except ValueError:
        return Response({'message' : 'Days Have To Be A Number'})

class TransactiondataCreateApiView(generics.CreateAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class TransactiondataDestroyApiView(generics.DestroyAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class RecurringBillsCreateApiView(generics.CreateAPIView):
    queryset = RecurringBills.objects.all()
    serializer_class = RecurringBillsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class RecurringBillsDestroyApiView(generics.DestroyAPIView):
    queryset = RecurringBills.objects.all()
    serializer_class = RecurringBillsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class BudgetCreateApiView(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BudgetDestroyApiView(generics.DestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
        

def monthly_average(request):
    expense_average = Transaction_data.objects.annotate(month = TruncMonth('date')).filter(user_id = request.user, transaction_type='expense').values('month').annotate(monthly_total = Sum('price')).aggregate(avg = Avg('monthly_total'))
    Income_average = Transaction_data.objects.annotate(month = TruncMonth('date')).filter(user_id = request.user, transaction_type='income').values('month').annotate(monthly_total = Sum('price')).aggregate(avg = Avg('monthly_total'))
    if expense_average['avg'] is None:
        expense_average['avg'] = 0
    if Income_average['avg'] is None:
        Income_average['avg'] = 0
    expense_mean, income_mean = round(expense_average['avg'],2),round(Income_average['avg'],2)
    return {'expense_average': expense_mean, 'income_average' : income_mean}


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filtering_expenses(request):
    serializer = FilteredExpansesInputSerializer(data = request.query_params)
    if serializer.is_valid():
        fields_dictionary = {}
        if serializer.data.get('from_date'):
            fields_dictionary['date__gte'] = serializer.data.get('from_date').strip()
        if serializer.data.get('to_date'):
            fields_dictionary['date__lte'] = serializer.data.get('to_date').strip()
        if serializer.data.get('category'):
            fields_dictionary['category'] = serializer.data.get('category').strip().lower()
        if serializer.data.get('transaction_type').strip().lower():
            fields_dictionary['transaction_type'] = serializer.data.get('transaction_type')
        serialized_data = ItemSerializer(Transaction_data.objects.filter(user_id=request.user, **fields_dictionary).order_by('-date'), many = True)
        return Response(serialized_data.data, status = 200)
    return Response({'message':'Invalid Input'}, status = 409)


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


def sum_of_transactions_analytics(request):
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
    return {'daily_expense' : expense_dates,'daily_income' : income_dates}


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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_budget(request):
    budget = SecondaryBudgetSerializer(Budget.objects.filter(user_id = request.user), many = True)
    for i in budget.data:
        transactions = Transaction_data.objects.filter(user_id=request.user, date__gte=i['date'], category=i['category'], transaction_type='expense').values('category').annotate(category_sum = Sum('price')).values('category_sum')
        if transactions:
            i['category_sum'] = transactions[0]['category_sum']
            if transactions[0]['category_sum'] < float(i['budget']):
                i['status'] = f'You Are Under Budget By {float(i['budget']) - float(transactions[0]['category_sum'])}'
            else:
                i['status'] = 'You Are Over Budget'
        else:
            i['category_sum'] = 0
            i['status'] = 'You Are Under Budget'
    return Response(budget.data)


def average_total_income_expenses_analytics(request):
    days = int(request.query_params.get('days',30))
    income_average = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='income').aggregate(income_average = Avg('price'))['income_average']
    expense_average = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='expense').aggregate(expense_average = Avg('price'))['expense_average']
    total_income = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='income').aggregate(total_income= Sum('price'))['total_income']
    total_expense = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days = days), transaction_type='expense').aggregate(total_expense = Sum('price'))['total_expense']
    return {'income_average': income_average, 'expense_average' : expense_average, 'total_income' : total_income, 'total_expense' : total_expense}


def data_for_piechart_analytics(request):
    days = int(request.query_params.get('days', 30))
    grouped_by_category = Transaction_data.objects.filter(user_id=request.user, date__gt = timezone.now().date() - timedelta(days=days), transaction_type='expense').values('category').annotate(stats = Sum('price'))
    return grouped_by_category


def data_for_piechart_total(request):
    grouped_by_category = Transaction_data.objects.filter(user_id=request.user, transaction_type='expense').values('category').annotate(stats = Sum('price'))
    return grouped_by_category


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def log_out(request):
    if request.data.get('refresh'):
        for_blacklist = RefreshToken(request.data['refresh'])
        for_blacklist.blacklist()
        return Response({'message' : 'logout successful'}, status=205)
    return Response({'message' : 'invalid'}, status=400)

@api_view(['POST'])
def register(request):
    serialized_register = RegisterInputSerializer(data = request.data)
    if serialized_register.is_valid():
        try:
            user = User.objects.create_user(username = serialized_register.data['username'], password = serialized_register.data['password'])
            return Response(status = 201)
        except IntegrityError:
            return Response({'message' : 'Username Is Already In Use'}, status = 409)
        except ValueError:
            return Response({'message' : 'Username Is Missing'}, status = 409)
    return Response(serialized_register.errors)
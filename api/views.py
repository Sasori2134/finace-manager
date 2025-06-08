from rest_framework.decorators import api_view, permission_classes, authentication_classes
from practice_project.serializers import ItemSerializer, FilteredExpansesSerializer, FilteredExpansesInputSerializer, BudgetSerializer, SecondaryBudgetSerializer, RecurringBillsSerializer
from rest_framework.response import Response
from .models import Transaction_data, Budget, RecurringBills
from django.db.models import Avg, Max, Sum
from django.db.models.functions import TruncMonth,TruncYear
from rest_framework import generics, permissions, authentication
from django.contrib.auth.models import User, auth
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def recurring_bills_function(user_id):
        recurring_bills = RecurringBillsSerializer(RecurringBills.objects.filter(user_id=user_id), many=True)
        for i in recurring_bills.data:
            transaction_data = ItemSerializer(Transaction_data.objects.filter(user_id=user_id, category=i['category'],itemname='recurring_bill',transaction_type='expense').order_by('-date'), many = True)
            if transaction_data.data:
                date = datetime.strptime(transaction_data.data[0]['date'],'%Y-%m-%d').strftime('%Y-%m')
                if timezone.now().date().day >= i['date'] and date != timezone.now().date().strftime('%Y-%m'):
                    i['date'] = timezone.now().date()
                    serialized_data = ItemSerializer(data = i)
                    if serialized_data.is_valid():
                        serialized_data.save()
            else:
                if timezone.now().date().day >= i['date']:
                    i['date'] = timezone.now().date()
                    serialized_data = ItemSerializer(data = i)
                    if serialized_data.is_valid():
                        serialized_data.save()

                    
class TransactiondataCreateApiView(generics.CreateAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class TransactiondataDeleteApiView(generics.DestroyAPIView):
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
        

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def monthly_average(request, user_id):
    expense_average = Transaction_data.objects.annotate(month = TruncMonth('date')).filter(user_id = user_id, transaction_type='expense').values('month').annotate(monthly_total = Sum('price')).aggregate(avg = Avg('monthly_total'))
    Income_average = Transaction_data.objects.annotate(month = TruncMonth('date')).filter(user_id=user_id, transaction_type='income').values('month').annotate(monthly_total = Sum('price')).aggregate(avg = Avg('monthly_total'))
    if expense_average['avg'] is None:
        expense_average['avg'] = 0
    if Income_average['avg'] is None:
        Income_average['avg'] = 0
    expense_mean, income_mean = round(expense_average['avg'],2),round(Income_average['avg'],2)
    return Response({'expense_average': expense_mean, 'income_average' : income_mean}, status=200)


# aq ginda date-dan date-mde shecvale mere exla mushaobs ragac pontshi XD
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filtering_expenses(request, user_id):
    serializer = FilteredExpansesInputSerializer(data = request.query_params)
    if serializer.is_valid():
        if serializer.validated_data.get('date') is None and serializer.validated_data.get('category') is None:
            filtered = Transaction_data.objects.filter(user_id=user_id).order_by('-date')
            serialized = FilteredExpansesSerializer(filtered,many=True)
        elif serializer.validated_data.get('date') is None:
            filtered = Transaction_data.objects.filter(user_id=user_id, category= serializer.validated_data.get('category')).order_by('-date')
            serialized = FilteredExpansesSerializer(filtered,many=True)
        elif serializer.validated_data.get('category') is None:
            filtered = Transaction_data.objects.filter(user_id=user_id, date=serializer.validated_data.get('date')).order_by('-date')
            serialized = FilteredExpansesSerializer(filtered, many=True)
        else:
            filtered = Transaction_data.objects.filter(user_id=user_id, date=serializer.validated_data.get('date'), category=serializer.validated_data.get('category')).order_by('-date')
            serialized = FilteredExpansesSerializer(filtered, many=True)
        #recurring bills
        recurring_bills_function(user_id)
        return Response(serialized.data)
    return Response({'message':'Invalid Input'}, status = 409)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def sum_of_transactions(request, user_id):
    grouped_by_month_expense = Transaction_data.objects.annotate(year = TruncYear('date')).filter(user_id=user_id, transaction_type='expense',year = timezone.now().date().replace(day=1,month=1)).annotate(month = TruncMonth('date')).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    grouped_by_month_income = Transaction_data.objects.annotate(year = TruncYear('date')).filter(user_id=user_id, transaction_type='income',year = timezone.now().date().replace(day=1,month=1)).annotate(month = TruncMonth('date')).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    return Response({'monthly_expense' : grouped_by_month_expense,'monthly_income' : grouped_by_month_income})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def total_balance_income_expenses(request):
    print(request.user)
    expenses = Transaction_data.objects.filter(user_id=request.user, transaction_type='expense').aggregate(price = Sum('price'))
    income = Transaction_data.objects.filter(user_id=request.user, transaction_type='income').aggregate(income = Sum('price'))
    if expenses['price'] is None:
        expenses['price'] = 0
    if income['income'] is None:
        income['income'] = 0
    balance = round(income['income'] - expenses['price'],2)
    return Response({'balance': balance, 'total_income' : income['income'], 'total_expense' : expenses['price']})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def recent_transactions(request,user_id):
    transactions = ItemSerializer(Transaction_data.objects.filter(user_id=user_id).order_by('-date')[:5], many=True)
    return Response({'recent_transactions' : transactions.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_budget(request, user_id):
    budget = SecondaryBudgetSerializer(Budget.objects.filter(user_id = user_id), many = True)
    for i in budget.data:
        transactions = Transaction_data.objects.filter(user_id=user_id, date__gte=i['date'], category=i['category'], transaction_type='expense').values('category').annotate(category_sum = Sum('price')).values('category_sum')
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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def average_total_income_expenses_analytics(request,user_id):
    from_date = dict(request.query_params)
    income_average = Transaction_data.objects.filter(user_id=user_id, date__gte = timezone.now().date() - timedelta(days = int(from_date['days'][0])), transaction_type='income').aggregate(income_average = Avg('price'))['income_average']
    expense_average = Transaction_data.objects.filter(user_id=user_id, date__gte = timezone.now().date() - timedelta(days = int(from_date['days'][0])), transaction_type='expense').aggregate(expense_average = Avg('price'))['expense_average']
    total_income = Transaction_data.objects.filter(user_id=user_id, date__gte = timezone.now().date() - timedelta(days = int(from_date['days'][0])), transaction_type='income').aggregate(total_income= Sum('price'))['total_income']
    total_expense = Transaction_data.objects.filter(user_id=user_id, date__gte = timezone.now().date() - timedelta(days = int(from_date['days'][0])), transaction_type='expense').aggregate(total_expense = Sum('price'))['total_expense']
    return Response({'income_average': income_average, 'expense_average' : expense_average, 'total_income' : total_income, 'total_expense' : total_expense})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def data_for_piechart_analytics(request, user_id):
    from_date = dict(request.query_params)
    grouped_by_category = Transaction_data.objects.filter(user_id=user_id, date__gte = timezone.now().date() - timedelta(days=int(from_date['days'][0])), transaction_type='expense').values('category').annotate(stats = Sum('price'))
    return Response(grouped_by_category)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def data_for_piechart_total(request,user_id):
    grouped_by_category = Transaction_data.objects.filter(user_id=user_id, transaction_type='expense').values('category').annotate(stats = Sum('price'))
    return Response(grouped_by_category)


@api_view(['POST'])
def register(request):
    try:
        user = User.objects.create_user(username = request.data['username'], password = request.data['password'])
        return Response(status = 201)
    except:
        return Response({'message' : 'Username Is Already In Use'}, status = 409)
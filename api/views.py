from rest_framework.decorators import api_view
from practice_project.serializers import ItemSerializer, IncomeSerializer, FilteredExpansesSerializer, FilteredExpansesInputSerializer, BudgetSerializer, SecondaryBudgetSerializer, RecurringBillsSerializer
from rest_framework.response import Response
from .models import Transaction_data, Income, Budget, RecurringBills
from django.db.models import Avg, Max, Sum
from django.db.models.functions import TruncMonth,TruncYear
from rest_framework import generics, permissions, authentication
from django.contrib.auth.models import User, auth
from django.utils import timezone
from datetime import datetime


# Create your views here.
def recurring_bills_function(user_id):
        recurring_bills = RecurringBillsSerializer(RecurringBills.objects.filter(user_id=user_id), many=True)
        for i in recurring_bills.data:
            transaction_data = ItemSerializer(Transaction_data.objects.filter(user_id=user_id, category=i['category'],itemname='recurring_bill').order_by('-date'), many = True)
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
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]


class TransactiondataDeleteApiView(generics.DestroyAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
        

@api_view(['GET'])
def average_max(request, user_id):
    spending_average_max = Transaction_data.objects.filter(user_id = user_id).aggregate(avg = Avg('price'), max = Max('price'))
    Income_average_max = Income.objects.filter(user_id=user_id).aggregate(avg = Avg('income'), max = Max('income'))
    if spending_average_max['avg'] is None:
        spending_average_max['avg'] = 0
        spending_average_max['max'] = 0
    if Income_average_max['avg'] is None:
        Income_average_max['avg'] = 0
        Income_average_max['max'] = 0
    spending_mean, spending_maximum, income_mean, income_max = round(spending_average_max['avg'],2), spending_average_max['max'], Income_average_max['avg'], Income_average_max['max']
    return Response({'spending_average': spending_mean,'spending_max' : spending_maximum, 'income_average' : income_mean, 'income_max' : income_max}, status=200)


# aq ginda date-dan date-mde shecvale mere exla mushaobs ragac pontshi XD
@api_view(['GET'])
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
def sum_of_expenses(request, user_id):
    filering = Transaction_data.objects.filter(user_id=user_id)
    grouped_by_month = filering.annotate(month = TruncMonth('date')).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    grouped_by_day = filering.values('date').annotate(dayly_sum = Sum('price')).order_by('date')
    grouped_by_year = filering.annotate(year = TruncYear('date')).values('year').annotate(yearly_sum = Sum('price')).order_by('year')
    return Response({'month' : grouped_by_month, 'day' : grouped_by_day, 'year' : grouped_by_year})

#swirdeba gadacema listis am incomebis
class AddIncomeCreateApiView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class IncomeDestroyApiView(generics.DestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


@api_view(['GET'])
def balance(request, user_id):
    expenses = Transaction_data.objects.filter(user_id=user_id).aggregate(price = Sum('price'))
    income = Income.objects.filter(user_id=user_id).aggregate(income = Sum('income'))
    if expenses['price'] is None:
        expenses['price'] = 0
    if income['income'] is None:
        income['income'] = 0
    balance = round(income['income'] - expenses['price'],2)
    return Response({'balance': balance})


@api_view(['GET'])
def this_month_sum(request, user_id):
        expenses = Transaction_data.objects.filter(user_id = user_id).values('price')[:30]
        income = Income.objects.filter(user_id = user_id).values('income')[:30]
        return Response({'expenses' : sum([i['price'] for i in expenses]), 'income' : sum([i['income'] for i in income])})


class BudgetCreateApiView(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class BudgetDestroyApiView(generics.DestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


@api_view(['GET'])
def get_budget(request, user_id):
    budget = SecondaryBudgetSerializer(Budget.objects.filter(user_id = user_id), many = True)
    for i in budget.data:
        transactions = Transaction_data.objects.filter(user_id=user_id, date__gte=i['date'], category=i['category']).values('category').annotate(category_sum = Sum('price')).values('category_sum')
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


class RecurringBillsCreateApiView(generics.CreateAPIView):
    queryset = RecurringBills.objects.all()
    serializer_class = RecurringBillsSerializer


class RecurringBillsDestroyApiView(generics.DestroyAPIView):
    queryset = RecurringBills.objects.all()
    serializer_class = RecurringBillsSerializer


@api_view(['POST'])
def login(request):
    user = auth.authenticate(username = request.data['username'], password = request.data['password'])
    if user is not None:
        return Response(status = 200)
    else:
        return Response({'message' : 'Username Or Password Is Invalid Please Try Again'}, status = 409)


@api_view(['POST'])
def register(request):
    try:
        user = User.objects.create_user(username = request.data['username'], password = request.data['password'])
        return Response(status = 201)
    except:
        return Response({'message' : 'Username Is Already In Use'}, status = 409)
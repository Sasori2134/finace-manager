from rest_framework.decorators import api_view
from practice_project.serializers import ItemSerializer, IncomeSerializer, FilteredExpansesSerializer, FilteredExpansesInputSerializer, BudgetSerializer
from rest_framework.response import Response
from .models import Transaction_data, Income, Budget
from django.db.models import Avg, Max, Sum
from django.db.models.functions import TruncMonth,TruncYear
from rest_framework import generics, permissions, authentication
from django.contrib.auth.models import User, auth


# Create your views here.
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
            filtered = Transaction_data.objects.filter(user_id=user_id)
            serialized = FilteredExpansesSerializer(filtered,many=True)
        elif serializer.validated_data.get('date') is None:
            filtered = Transaction_data.objects.filter(user_id=user_id, category= serializer.validated_data.get('category'))
            serialized = FilteredExpansesSerializer(filtered,many=True)
        else:
            filtered = Transaction_data.objects.filter(user_id=user_id, date=serializer.validated_data.get('date'), category=serializer.validated_data.get('category'))
            serialized = FilteredExpansesSerializer(filtered, many=True)
        return Response(serialized.data)
    return Response({'message':'Invalid Input'}, status = 409)


@api_view(['GET'])
def sum_of_expenses(request, user_id):
    filering = Transaction_data.objects.filter(user_id=user_id)
    grouped_by_month = filering.annotate(month = TruncMonth('date')).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    grouped_by_day = filering.values('date').annotate(dayly_sum = Sum('price')).order_by('date')
    grouped_by_year = filering.annotate(year = TruncYear('date')).values('year').annotate(yearly_sum = Sum('price')).order_by('year')
    return Response({'month' : grouped_by_month, 'day' : grouped_by_day, 'year' : grouped_by_year})


class AddIncomeCreateApiView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET'])
def balance(request, user_id):
    expenses = Transaction_data.objects.filter(user_id=user_id).aggregate(price = Sum('price'))
    income = Income.objects.filter(user_id=user_id).aggregate(income = Sum('income'))
    if expenses['price'] is None:
        expenses['price'] = 0
    if income['income'] is None:
        income['income'] = 0
    if income['income'] is not None and expenses['price'] is not None:
        balance = round(income['income'] - expenses['price'],2)
        return Response({'balance': balance})


@api_view(['GET'])
def last_30_days(request, user_id):
    if request.query_params['how'] == 'sum':
        expenses = Transaction_data.objects.filter(user_id = user_id).values('price')[:30]
        income = Income.objects.filter(user_id = user_id).values('income')[:30]
        return Response({'expenses' : sum([i['price'] for i in expenses]), 'income' : sum([i['income'] for i in income])})
    elif request.query_params['how'] == 'list':
        expenses = Transaction_data.objects.filter(user_id=user_id).values('date').annotate(dayly_sum = Sum('price')).order_by('date')[:30]
        income = Income.objects.filter(user_id=user_id).values('date').annotate(daily_income = Sum('income'))[:30]
        return Response({'expenses' : expenses,'income' : income})
    else:
        return Response({'message' : 'Wrong Option'}, status=409)


class BudgetCreateApiView(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

#shecvale Responsebi es raari
@api_view(['GET'])
def check_budget(request, user_id):
    expenses = Transaction_data.objects.filter(user_id = user_id).values('price')[::-1][:30]
    budget = Budget.objects.filter(user_id = user_id).values('budget')[0]
    sum_of_expenses = sum([i['price'] for i in expenses])
    if sum_of_expenses < budget['budget']:
        return Response({'message' : 'all good'},status = 200)
    else:
        return Response({'message' : 'you went over your budget btw'}, status=200)
        

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
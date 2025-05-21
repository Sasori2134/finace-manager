from rest_framework.decorators import api_view
from practice_project.serializers import ItemSerializer, IncomeSerializer, FilteredExpansesSerializer, FilteredExpansesInputSerializer
from rest_framework.response import Response
from .models import Transaction_data, Income
from django.db.models import Avg, Max, Sum
from django.db.models.functions import TruncMonth,TruncYear
from rest_framework import generics, permissions, authentication
from django.contrib.auth.models import User, auth


# Create your views here.
# aq abrunebs datas rasac agzavnis user gadaakete create() momavalshi
class TransactiondataCreateApiView(generics.CreateAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self,serializer):
        serializer.save()


class TransactiondataDeleteApiView(generics.DestroyAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
        


@api_view(['GET'])
def average_max(request, user_id):
    spending_average = Transaction_data.objects.filter(user_id = user_id).aggregate(avg = Avg('price'), max = Max('price'))
    mean, maximum = round(spending_average['avg'],2), spending_average['max']
    return Response({'average': mean,'max' : maximum}, status=200)


# aq ginda date-dan date-mde shecvale mere exla mushaobs ragac pontshi XD
@api_view(['GET'])
def filtering_expenses(request, user_id):
    serializer = FilteredExpansesInputSerializer(data = request.data)
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


#shecvale es sum_of_expanses
@api_view(['GET'])
def sum_of_values(request,user_id):
    filering = Transaction_data.objects.filter(user_id=user_id)
    grouped_by_month = filering.annotate(month = TruncMonth('date')).values('month').annotate(monthly_sum = Sum('price')).order_by('month')
    grouped_by_day = filering.values('date').annotate(dayly_sum = Sum('price')).order_by('date')
    grouped_by_year = filering.annotate(year = TruncYear('date')).values('year').annotate(yearly_sum = Sum('price')).order_by('year')
    return Response({'month' : grouped_by_month, 'day' : grouped_by_day, 'year' : grouped_by_year})


# aq abrunebs datas rasac agzavnis user gadaakete create() momavalshi
class AddIncomeCreateApiView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def perform_create(self,serializer):
        serializer.save()


#rodesac ar aris income an expense sheyvanili abrunebs mesijs Balance not avaliable gaaswore ise rom tu ar aris sheyvanili mashin 0 iyos
@api_view(['GET'])
def balance(request,user_id):
    expenses = Transaction_data.objects.filter(user_id=user_id).aggregate(price = Sum('price'))
    income = Income.objects.filter(user_id=user_id).aggregate(income = Sum('income'))
    if income['income'] and expenses['price']:
        balance = round(income['income'] - expenses['price'],2)
        return Response({'balance': balance})
    return Response({'message' : 'Balance Not Avaliable'})


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
        return Response(status = 200)
    except:
        return Response({'message' : 'Username Is Already In Use'}, status = 409)

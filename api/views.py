from rest_framework.decorators import api_view, permission_classes, authentication_classes
from Finance_Manager.serializers import ItemSerializer, FilteredExpansesSerializer, FilteredExpansesInputSerializer, BudgetSerializer, RecurringBillsSerializer, RegisterInputSerializer
from rest_framework.response import Response
from .models import Transaction_data, Budget, RecurringBills
from django.db.models import Sum
from rest_framework import generics
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination


# Create your views here.
# unda gavaketo tavidan dzaan hardcoded ari
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def recurring_bills_function(request):
    recurring_bills = RecurringBillsSerializer(RecurringBills.objects.filter(user_id=request.user), many=True)
    for i in recurring_bills.data:
        transaction_data = ItemSerializer(Transaction_data.objects.filter(user_id=request.user, category=i['category'],itemname='recurring_bill',transaction_type='expense').order_by('-date'), many = True)
        if transaction_data.data:
            date = datetime.strptime(transaction_data.data[0]['date'],'%Y-%m-%d').strftime('%Y-%m')
            if timezone.now().date().day >= i['date'] and date != timezone.now().date().strftime('%Y-%m'):
                i['date'] = timezone.now().date()
                serialized_data = ItemSerializer(data = i, context = {'request' : request})
                if serialized_data.is_valid():
                    serialized_data.save()
        else:
            if timezone.now().date().day >= i['date']:
                i['date'] = timezone.now().date()
                serialized_data = ItemSerializer(data = i, context = {'request' : request})
                if serialized_data.is_valid():
                    serialized_data.save()
    return Response(status=200)


class TransactiondataCreateApiView(generics.CreateAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serialized_data = self.get_serializer(data = request.data)
        serialized_data.is_valid(raise_exception=True)
        self.perform_create(serialized_data)
        return Response({'pk' : serialized_data.data['pk']})

class TransactiondataDestroyApiView(generics.DestroyAPIView):
    queryset = Transaction_data.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction_data.objects.filter(user_id=self.request.user)


class RecurringBillsCreateApiView(generics.CreateAPIView):
    queryset = RecurringBills.objects.all()
    serializer_class = RecurringBillsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serialized_data = self.get_serializer(data = request.data)
        serialized_data.is_valid(raise_exception=True)
        self.perform_create(serialized_data)
        return Response({'pk' : serialized_data.data['pk']})


class RecurringBillsDestroyApiView(generics.DestroyAPIView):
    queryset = RecurringBills.objects.all()
    serializer_class = RecurringBillsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecurringBills.objects.filter(user_id=self.request.user)

class BudgetCreateApiView(generics.CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serialized_data = self.get_serializer(data = request.data)
        serialized_data.is_valid(raise_exception=True)
        self.perform_create(serialized_data)
        return Response({'pk' : serialized_data.data['pk']})


class BudgetDestroyApiView(generics.DestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user_id=self.request.user)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_recurring_bills(request):
    recurring_bills = RecurringBills.objects.filter(user_id=request.user)
    serialized = RecurringBillsSerializer(recurring_bills, many=True)
    return Response(serialized.data)


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
            fields_dictionary['category__iexact'] = serializer.data.get('category').strip().lower()
        if serializer.data.get('transaction_type'):
            if serializer.data.get('transaction_type').strip().lower() in ['expense','income']:
                fields_dictionary['transaction_type'] = serializer.data.get('transaction_type').strip().lower()
        data = Transaction_data.objects.filter(user_id=request.user, **fields_dictionary).order_by('-date')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(data,request)
        serialized_data = FilteredExpansesSerializer(page, many = True)

        return paginator.get_paginated_response(serialized_data.data)
    return Response({'message':'Invalid Input'}, status = 400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_budget(request):
    budget = BudgetSerializer(Budget.objects.filter(user_id = request.user).order_by('-date'), many = True)
    for i in budget.data:
        transactions = Transaction_data.objects.filter(user_id=request.user, date__gte=i['date'], category__iexact=i['category'], transaction_type='expense').values('category').annotate(spent = Sum('price')).values('spent')
        if transactions:
            i['spent'] = transactions[0]['spent']
            if i.get('spent',0) < float(i['budget']):
                i['status'] = f'You Are Under Budget By {float(i['budget']) - float(i['spent'])}'
            else:
                i['status'] = 'You Are Over Budget'
        else:
            i['spent'] = 0
            i['status'] = 'You Are Under Budget'
    return Response(budget.data)


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
    if serialized_register.is_valid(raise_exception=True):
        user = User.objects.create_user(username = serialized_register.data['username'], password = serialized_register.data['password'])
        return Response(status = 201)
    return Response(serialized_register.errors)
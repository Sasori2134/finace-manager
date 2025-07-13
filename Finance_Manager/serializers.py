from rest_framework import serializers
from api.models import Transaction_data, Budget, RecurringBills
from .functions import check_float
from rest_framework import validators
from django.contrib.auth.models import User
from .functions import check_float, validation_dictionary
from decimal import Decimal


class ItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits = 10, min_value=Decimal('0.01'), decimal_places=2, error_messages=validation_dictionary("DecimalField", 'price'))
    category = serializers.CharField(max_length = 50, error_messages=validation_dictionary("CharField", "category"))
    itemname = serializers.CharField(max_length = 200, error_messages=validation_dictionary("CharField", "item name"))
    transaction_type = serializers.CharField(max_length=8, min_length=6, error_messages=validation_dictionary("CharField", "transaction_type", min_length=6))
    class Meta:
        model = Transaction_data

        fields = [
            'pk',
            'date',
            'category',
            'itemname',
            'price',
            'transaction_type'
        ]
        
    def validate(self, data):
        data['category'] = data['category'].strip().lower()
        data['itemname'] = data['itemname'].strip().lower()
        data['transaction_type'] = data['transaction_type'].strip().lower()
        if data.get('transaction_type') not in ['expense','income']:
            raise serializers.ValidationError('You Have To Input Valid Transaction Type')
        if data.get('category').isdigit() or check_float(data.get('category')):
            raise serializers.ValidationError("Category Can't Be A Number")
        if data.get('itemname').isdigit() or check_float(data.get('itemname')):
            raise serializers.ValidationError("Item Can't Be A Number")
        return data
        
    def create(self, validated_data):
        return Transaction_data.objects.create(user_id=self.context['request'].user, **validated_data)
        
        

class FilteredExpansesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_data

        fields = [
            'pk',
            'itemname',
            'price',
            'date',
            'category',
            'transaction_type'
        ]


class FilteredExpansesInputSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=False, allow_null=True)
    to_date = serializers.DateField(required=False, allow_null=True)
    category = serializers.CharField(max_length=50,required=False, allow_null=True)
    transaction_type = serializers.CharField(max_length=7, required=False, allow_null=True)


class BudgetSerializer(serializers.ModelSerializer):
    budget = serializers.DecimalField(max_digits = 10, decimal_places=2, min_value=Decimal('0.01'), error_messages=validation_dictionary("DecimalField",'Budget'))
    category = serializers.CharField(max_length=50,error_messages=validation_dictionary("CharField", "Category"))

    class Meta:
        model = Budget

        fields = [
            'pk',
            'budget',
            'category',
            'date'
        ]

    def validate(self, data):
        user = self.context['request'].user
        data['category'] = data['category'].strip().lower()
        if Budget.objects.filter(user_id=user, category=data.get('category')).exists():
            raise serializers.ValidationError('Category Already Exists')
        if data.get('category').isdigit() or check_float(data.get('category')):
            raise serializers.ValidationError('You Have To Include Valid Category')
        return data


    def create(self, validated_data):
        return Budget.objects.create(user_id=self.context['request'].user, **validated_data)



class RecurringBillsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=50,error_messages=validation_dictionary("CharField", "Category"))

    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'), error_messages=validation_dictionary("DecimalField", "Price"))

    date = serializers.IntegerField(min_value=1, max_value=31,error_messages={
        'invalid' : 'You Have To Include Valid Day',
        'min_value' : 'Day Has To Be More Than Zero',
        'max_value' : 'Day Cant Be More Than 31'
    })
    class Meta:
        model = RecurringBills

        fields = [
            'pk',
            'category',
            'itemname',
            'price',
            'date',
            'transaction_type'
        ]

    def validate(self, data):
        data['category'] = data['category'].strip().lower()
        user = self.context['request'].user
        if data.get('category').isdigit() or check_float(data.get('category')):
            raise serializers.ValidationError("Invalid Input: Category Can't Be A Number")
        elif RecurringBills.objects.filter(user_id=user, category= data.get('category')).exists():
            raise serializers.ValidationError('You Can Only Have One Recurring Bill On One Category')
        return data

    def create(self, validated_data):
        return RecurringBills.objects.create(user_id=self.context['request'].user, **validated_data)


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, min_length=3,validators=[validators.UniqueValidator(queryset=User.objects.all(), message="Username Already In Use")],error_messages=validation_dictionary("CharField", "Username",min_length=3))
    password = serializers.CharField(max_length=50, min_length=6,error_messages=validation_dictionary("CharField", "Password",min_length=6))

    def validate_username(self, value):
        if value.isdigit() or check_float(value):
            raise serializers.ValidationError("Username Can't Be A Number")
        return value

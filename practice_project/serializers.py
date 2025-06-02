from rest_framework import serializers
from api.models import Transaction_data, Income, Budget, RecurringBills
from .functions import check_float


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_data

        fields = [
            'user_id',
            'date',
            'category',
            'itemname',
            'price'
        ]
        
    def validate(self, data):
        # if data['price'] is not None and data['price'] != '':
        if data['price'] <= 0:
            raise serializers.ValidationError("Item Price Has To Be More Than 0")
        # else:
        #     raise serializers.ValidationError("You Have To Include A Price")
        if data['category'].isdigit() or check_float(data['category']):
            raise serializers.ValidationError("Category Can't Be A Number")
        else:
            if not data['category']:
                data['category'] = 'unknown'
            data['category'] = data['category'].strip().lower()
        if data['itemname'].isdigit() or check_float(data['itemname']):
            raise serializers.ValidationError("Item Can't Be A Number")
        else:
            if not data['itemname']:
                data['itemname'] = 'unknown'
            data['itemname'] = data['itemname'].strip().lower()
        return data
        

class FilteredExpansesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_data

        fields = [
            'pk',
            'itemname',
            'price',
            'date',
            'category',
        ]


class FilteredExpansesInputSerializer(serializers.Serializer):
    date = serializers.DateField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income

        fields = [
            'pk',
            'user_id',
            'income',
            'date'
        ]


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget

        fields = [
            'user_id',
            'budget',
            'category',
            'date'
        ]

    def validate(self, data):
        user = self.initial_data['user_id']
        if Budget.objects.filter(user_id=user, category=data['category']).exists():
            raise serializers.ValidationError('Category Already Exists')
        if not data['budget']:
            raise serializers.ValidationError('You Have To Include Budget')
        if not data['category'] or data['category'].isdigit() or check_float(data['category']):
            raise serializers.ValidationError('You Have To Include Category')
        else:
            data['category'] = data['category'].strip().lower()
        return data


class SecondaryBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget

        fields = [
            'pk',
            'budget',
            'category',
            'date'
        ]


class RecurringBillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringBills

        fields = [
            'pk',
            'user_id',
            'category',
            'itemname',
            'price',
            'date'
        ]

    def validate(self, data):
        if data['category']:
            data['category'] = data['category'].strip().lower()
            user = self.initial_data['user_id']
            if RecurringBills.objects.filter(user_id=user, category= data['category']).exists():
                raise serializers.ValidationError('You Can Only Have One Recurring Bill On One Category')
            elif data['category'].isdigit() or check_float(data['category']):
                raise serializers.ValidationError("Invalid Input: Category Can't Be A Number")
        else:
            raise serializers.ValidationError("You Have To Include Category")
        if data['price'] <= 0:
            raise serializers.ValidationError("Price Has To Be More Than 0")
        if data['date'] == 0 or data['date'] > 31:
            raise serializers.ValidationError("Date Can't Be More Than Less Than 0 Or More Than 31")
        return data

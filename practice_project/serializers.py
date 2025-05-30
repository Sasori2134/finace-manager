from rest_framework import serializers
from api.models import Transaction_data, Income, Budget, RecurringBills


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
        if data['price'] <= 0:
            raise serializers.ValidationError("Item Price Can't be Less Than 0")
        if not data['category']:
            data['category'] = 'unknown'
        if not data['itemname']:
            data['itemname'] = 'unknown'
        if not data['price']:
            raise Serializers.ValidationError('You Have To Include Price')
        else:
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
        if not data['category']:
            raise serializers.ValidationError('You Have To Include Category')
        else:
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
    def validate_category(self, value):
        user = self.initial_data['user_id']
        if RecurringBills.objects.filter(user_id=user, category=value).exists():
            raise serializers.ValidationError('You Can Only Have One Recurring Bill On One Category')
        else:
            return value
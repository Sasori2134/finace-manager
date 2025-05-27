from rest_framework import serializers
from api.models import Transaction_data, Income, Budget


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
    def validate_price(self, value):
        if value <= 0:
            raise ValueError("Item Price Can't be Less Than 0")
        else:
            return value

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
    def validate_category(self, value):
        user = self.initial_data['user_id']
        if Budget.objects.filter(user_id=user, category=value).exists():
            raise serializers.ValidationError('Category Already Exists')
        else:
            return value


class SecondaryBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'budget',
            'category',
            'date'
        ]
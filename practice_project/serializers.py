from rest_framework import serializers
from api.models import Transaction_data, Income


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


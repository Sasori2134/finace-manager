from rest_framework import serializers
from api.models import Transaction_data, Budget, RecurringBills
from .functions import check_float


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_data

        fields = [
            'user_id',
            'date',
            'category',
            'itemname',
            'price',
            'transaction_type'
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
            'transaction_type'
        ]


class FilteredExpansesInputSerializer(serializers.Serializer):
    date = serializers.DateField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget

        fields = [
            'budget',
            'category',
            'date'
        ]

    def validate(self, data):
        user = self.context['request'].user
        if Budget.objects.filter(user_id=user, category=data['category']).exists():
            raise serializers.ValidationError('Category Already Exists')
        if not data.get('budget'):
            raise serializers.ValidationError('You Have To Include Budget')
        if not data.get('category') or data.get('category').isdigit() or check_float(data.get('category')):
            raise serializers.ValidationError('You Have To Include Category')
        return data
    def create(self, validated_data):
        return Budget.objects.create(user_id=self.context['request'].user, **validated_data)


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

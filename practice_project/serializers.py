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
        if data.get('price') <= 0:
            raise serializers.ValidationError("Item Price Has To Be More Than 0")
        if data.get('category').isdigit() or check_float(data.get('category')):
            raise serializers.ValidationError("Category Can't Be A Number")
        else:
            if not data.get('category'):
                data['category'] = 'unknown'
        if data.get('itemname').isdigit() or check_float(data.get('itemname')):
            raise serializers.ValidationError("Item Can't Be A Number")
        else:
            if not data.get('itemname'):
                data['itemname'] = 'unknown'
        return data
        
    def create(self, validated_data):
        return Transaction_data.objects.create(user_id=self.context['user'], **validated_data)
        

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
            'category',
            'itemname',
            'price',
            'date',
            'transaction_type'
        ]

    def validate(self, data):
        if data.get('category'):
            data['category'] = data['category'].strip().lower()
            user = self.context['request'].user
            if data['category'].isdigit() or check_float(data['category']):
                raise serializers.ValidationError("Invalid Input: Category Can't Be A Number")
            elif RecurringBills.objects.filter(user_id=user, category= data['category']).exists():
                raise serializers.ValidationError('You Can Only Have One Recurring Bill On One Category')
        else:
            raise serializers.ValidationError("You Have To Include Category")
        if not data.get('price'):
            raise serializers.ValidationError("You Have To Include Price")
        elif data.get('price') <= 0:
            raise serializers.ValidationError("Price Has To Be More Than 0")
        if not data.get('date'):
            raise serializers.ValidationError("You Have To Include Date")
        elif data.get('date') == 0 or data.get('date') > 31:
            raise serializers.ValidationError("Date Can't Be More Than Less Than 0 Or More Than 31")
        return data
    def create(self, validated_data):
        return RecurringBills.objects.create(user_id=self.context['request'].user, **validated_data)


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=50, allow_blank = True)

    def validate_password(self,value):
        if not value:
            raise serializers.ValidationError('Password is Missing')
        else:
            return value
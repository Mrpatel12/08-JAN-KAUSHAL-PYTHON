from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    farm = serializers.ReadOnlyField(source='farm.id')

    class Meta:
        model = Expense
        fields = ('id', 'farm', 'crop', 'category', 'amount', 'currency', 'occurred_at', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'farm', 'created_at', 'updated_at')

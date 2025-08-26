from rest_framework import serializers
from expenses.models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ["id", "date", "user"]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Expense.objects.create(**validated_data)

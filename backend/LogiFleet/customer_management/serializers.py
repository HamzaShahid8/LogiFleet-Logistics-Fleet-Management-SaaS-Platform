from rest_framework import serializers
from .models import Customer

class CustomerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'code', 'name', 'email', 'phone', 'address', 'city', 'country', 'tax_number', 'credit_limit', 'created_at', 'updated_at']
        
class CustomerWriteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'country', 'tax_number', 'credit_limit']
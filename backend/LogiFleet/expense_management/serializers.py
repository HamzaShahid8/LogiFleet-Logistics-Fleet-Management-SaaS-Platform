from rest_framework import serializers
from .models import Expense
from shipping_management.models import Shipment
from driver_management.models import Driver
from vehicle_management.models import Vehicle
from django.utils import timezone

class ExpenseReadSerializer(serializers.ModelSerializer):
    shipment_number = serializers.CharField(source='shipment.shipment_number', read_only=True)
    driver_name = serializers.CharField(source='driver.full_name', read_only=True)
    vehicle_name = serializers.CharField(source='vehicle.registration_number', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            "id",
            "code",
            "expense_type",
            "shipment",
            'shipment_number',
            "driver",
            'driver_name',
            "vehicle",
            'vehicle_name',
            "amount",
            "payment_method",
            "description",
            "expense_date",
            "receipt_number",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        
class ExpenseWriteSerializer(serializers.ModelSerializer):
    shipment = serializers.SlugRelatedField(queryset = Shipment.objects.all(), slug_field='shipment_number')
    driver = serializers.SlugRelatedField(queryset = Driver.objects.all(), slug_field='full_name')
    vehicle = serializers.SlugRelatedField(queryset = Vehicle.objects.all(), slug_field='registration_number')
    
    class Meta:
        model = Expense
        fields = [
            "expense_type",
            "shipment",
            "driver",
            "vehicle",
            "amount",
            "payment_method",
            "description",
            "expense_date",
            "receipt_number",
        ]
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Expense amount must be greater than zero')
        return value
    
    def validate_expense_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError('Expense date cannot be in the future')
        return value
    
    def validate(self, attrs):
        
        shipment = attrs.get('shipment')
        driver = attrs.get('driver')
        vehicle = attrs.get('vehicle')
        
        if shipment:
            
            if shipment.is_deleted:
                raise serializers.ValidationError('Cannot add expense to the deleted shipment')
        
        if driver:
            
            if driver.is_deleted:
                raise serializers.ValidationError('Cannot use deleted driver')
            
        if vehicle:
            
            if vehicle.is_deleted:
                raise serializers.ValidationError('Cannot use deleted vehicle')
            
        return attrs
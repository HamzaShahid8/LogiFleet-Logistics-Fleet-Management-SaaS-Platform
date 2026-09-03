from rest_framework import serializers
from .models import Invoice
from customer_management.models import Customer
from shipping_management.models import *

class InvoiceReadSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    shipment_number = serializers.CharField(source='shipment.shipment_number', read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'code', 'invoice_number', 'customer', 'customer_name', 'shipment', 'shipment_number', 'issue_date', 'due_date', 'subtotal', 'total_amount', 'paid_amount', 'status', 'notes', 'is_deleted', 'created_at', 'updated_at']
        
class InvoiceWriteSerializer(serializers.ModelSerializer):
    shipment = serializers.SlugRelatedField(queryset = Shipment.objects.all(), slug_field='shipment_number')

    class Meta:
        model = Invoice
        fields = ['invoice_number', 'shipment', 'due_date', 'notes']
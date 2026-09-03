from rest_framework import serializers
from .models import Payment
from invoice_management.models import Invoice

class PaymentReadSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'code', 'payment_number', 'invoice', 'invoice_number', 'customer', 'customer_name', 'amount', 'payment_method', 'payment_date', 'reference_number', 'status', 'notes', 'is_deleted', 'created_at', 'updated_at']
        
class PaymentWriteSerializer(serializers.ModelSerializer):
    invoice = serializers.SlugRelatedField(queryset = Invoice.objects.all(), slug_field='invoice_number', write_only=True)
    
    class Meta:
        model = Payment
        fields = [ "invoice", "amount", "payment_method", "reference_number", "status", "notes"]
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero')
        return value
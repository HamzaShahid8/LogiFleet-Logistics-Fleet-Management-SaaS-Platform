from django.db import transaction
from invoice_management.models import Invoice
from rest_framework.exceptions import ValidationError
from .models import Payment, IdempotancyKey
from decimal import Decimal
from django.db.models import Sum
from .serializers import *

class PaymentService:
    
    @staticmethod
    @transaction.atomic
    def soft_delete(payment):
        payment.is_deleted = True
        payment.save(update_fields = ['is_deleted'])
        PaymentService.update_invoice(payment.invoice)
        return payment
    
    @staticmethod
    @transaction.atomic
    def restore(payment):
        payment.is_deleted = False
        payment.save(update_fields = ['is_deleted'])
        PaymentService.update_invoice(payment.invoice)
        return payment
    
    @staticmethod
    @transaction.atomic
    def create_payment(validated_data, user, idempotency_key):
        
        existing = IdempotancyKey.objects.filter(
            user=user,
            key=idempotency_key
        ).first()
        
        if existing:
            return existing.response_data, existing.status_code
        
        invoice = validated_data.pop('invoice')
        
        # lock
        invoice = (Invoice.objects.select_for_update().get(pk=invoice.pk))
        
        if invoice.is_deleted:
            raise ValidationError('Cannot create payment for deletd invoices')
        
        payment = Payment.objects.create(
            payment_number=f"PAY-{invoice.invoice_number}",
            invoice=invoice,
            customer=invoice.customer,
            **validated_data
        )
        
        PaymentService.update_invoice(invoice)
        
        response_data = PaymentReadSerializer(payment).data
        
        IdempotancyKey.objects.create(
            user=user,
            key=idempotency_key,
            response_data=response_data,
            status_code=201
        )
        
        return response_data, 201
    
    @staticmethod
    def update_invoice(invoice):
        paid_amount = (
            Payment.objects.filter(
                invoice=invoice,
                is_deleted=False,
                status='completed'
            )
            .aggregate(total = Sum('amount'))['total'] or Decimal('0.00')
        )
        
        invoice.paid_amount = paid_amount
        
        if paid_amount == 0:
            invoice.status = 'issued'
            
        elif paid_amount < invoice.total_amount:
            invoice.status = 'partially_paid'
            
        else:
            invoice.status = 'paid'
            
        invoice.save(update_fields = ['status', 'paid_amount', 'updated_at'])
        
        return invoice
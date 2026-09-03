from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal
from .models import Invoice
from datetime import timedelta

class InvoiceService:
    
    @staticmethod
    def soft_delete(invoice):
        invoice.is_deleted = True
        invoice.save(
            update_fields = ['is_deleted']
        )
        return invoice
    
    @staticmethod
    def restore(invoice):
        invoice.is_deleted = False
        invoice.save(
            update_fields = ['is_deleted']
        )
        return invoice
    
    @staticmethod
    @transaction.atomic
    def calculate_invoice(shipment):
        subtotal = (
            shipment.charges.filter(is_deleted = False).aggregate(total = Sum('amount'))['total'] or Decimal('0.00')
        )
        
        invoice = Invoice.objects.create(
            invoice_number=f"INV-{shipment.shipment_number}",
            customer=shipment.customer,
            shipment=shipment,
            due_date=timezone.now() + timedelta(days=7),
            subtotal=subtotal,
            total_amount=subtotal,
            status='issued',
        )
        return invoice

    @staticmethod
    @transaction.atomic
    def update_invoice(invoice):

        subtotal = (
            invoice.shipment.charges
            .filter(is_deleted=False)
            .aggregate(total=Sum('amount'))['total']
            or Decimal('0.00')
        )

        invoice.subtotal = subtotal
        invoice.total_amount = subtotal

        invoice.save(
            update_fields=[
                'subtotal',
                'total_amount',
                'updated_at'
            ]
        )

        return invoice
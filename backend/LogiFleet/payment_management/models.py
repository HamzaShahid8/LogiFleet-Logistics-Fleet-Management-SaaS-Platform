from django.db import models
from invoice_management.models import Invoice
from customer_management.models import Customer, UUID
from .managers import ActivePaymentManager, DeletedPaymentManager, AllPaymentManager
from accounts.models import BaseModel

class Payment(BaseModel, UUID):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("card", "Card"),
        ("online", "Online"),
        ("cheque", "Cheque"),
        ("other", "Other"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    payment_number = models.CharField(
        max_length=50,
        unique=True
    )

    invoice = models.ForeignKey(
        "invoice_management.Invoice",
        on_delete=models.PROTECT,
        related_name="payments"
    )

    customer = models.ForeignKey(
        "customer_management.Customer",
        on_delete=models.PROTECT,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    notes = models.TextField(
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
    
    objects = ActivePaymentManager()
    deleted_objects = DeletedPaymentManager()
    all_objects = AllPaymentManager()
    
    def __str__(self):
        return f"{self.payment_number} - {self.invoice.invoice_number} - {self.customer.name}"
    
class IdempotancyKey(models.Model):
    key = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payment_idempotancy')
    response_data = models.JSONField(blank=True, null=True)
    status_code = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.key
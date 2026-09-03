from django.db import models
from customer_management.models import UUID
from accounts.models import BaseModel
from .managers import ActiveInvoiceManager, AllInvoiceManager, DeletedInvoiceManager

class Invoice(BaseModel, UUID):

    INVOICE_STATUS_CHOICES = [
        ("draft", "Draft"),
        ("issued", "Issued"),
        ("partially_paid", "Partially Paid"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey(
        "customer_management.Customer",
        on_delete=models.PROTECT,
        related_name="invoices"
    )

    shipment = models.OneToOneField(
        "shipping_management.Shipment",
        on_delete=models.PROTECT,
        related_name="invoice"
    )

    issue_date = models.DateTimeField(
        auto_now_add=True
    )

    due_date = models.DateTimeField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS_CHOICES,
        default="draft"
    )

    notes = models.TextField(
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
    
    objects = ActiveInvoiceManager()
    deleted_objects = DeletedInvoiceManager()
    all_objects = AllInvoiceManager()
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer} - {self.shipment}"
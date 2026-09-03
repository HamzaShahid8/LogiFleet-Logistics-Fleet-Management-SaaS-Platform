from django.db import models
from accounts.models import BaseModel
from customer_management.models import UUID
from driver_management.models import Driver
from vehicle_management.models import Vehicle
from shipping_management.models import Shipment
from .managers import ActiveExpenseManager, DeletedExpenseManager, AllExpenseManager


class Expense(BaseModel, UUID):

    EXPENSE_TYPE_CHOICES = [
        ("fuel", "Fuel"),
        ("toll", "Toll"),
        ("parking", "Parking"),
        ("driver_allowance", "Driver Allowance"),
        ("maintenance", "Maintenance"),
        ("other", "Other"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
    ]

    expense_type = models.CharField(
        max_length=30,
        choices=EXPENSE_TYPE_CHOICES,
        default='other'
    )

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash"
    )

    description = models.TextField(
        blank=True
    )

    expense_date = models.DateTimeField()

    receipt_number = models.CharField(
        max_length=100,
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
    
    objects = ActiveExpenseManager()
    deleted_objects = DeletedExpenseManager()
    all_objects = AllExpenseManager()

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"
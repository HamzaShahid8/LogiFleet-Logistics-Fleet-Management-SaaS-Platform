from django.db import models
from accounts.models import BaseModel
from customer_management.models import UUID
from .managers import ActiveShipmentManager, DeletedShipmentManager, AllShipmentManager, ActiveShipmentChargeManager, DeletedShipmentChargeManager, AllShipmentChargeManager


class Shipment(BaseModel, UUID):
    
    SHIPMENT_STATUS = [
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("picked_up", "Picked Up"),
        ("in_transit", "In Transit"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]
    
    SHIPMENT_PRIORITY = [
        ("low", "Low"),
        ("normal", "Normal"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    shipment_number = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey('customer_management.Customer', on_delete=models.PROTECT, related_name='shipments')

    driver = models.ForeignKey(
        'driver_management.Driver',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="shipments"
    )

    vehicle = models.ForeignKey(
        'vehicle_management.Vehicle',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="shipments"
    )

    pickup_address = models.TextField()

    delivery_address = models.TextField()

    pickup_city = models.CharField(
        max_length=100
    )

    delivery_city = models.CharField(
        max_length=100
    )

    package_description = models.TextField()

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    priority = models.CharField(
        max_length=20,
        choices=SHIPMENT_PRIORITY,
        default='normal'
    )

    status = models.CharField(
        max_length=30,
        choices=SHIPMENT_STATUS,
        default='pending'
    )

    pickup_date = models.DateTimeField()

    estimated_delivery_date = models.DateTimeField()

    receiver_name = models.CharField(
        max_length=150,
        blank=True
    )

    receiver_phone = models.CharField(
        max_length=30,
        blank=True
    )

    delivery_notes = models.TextField(
        blank=True
    )

    failure_reason = models.TextField(
        blank=True
    )

    actual_delivery_date = models.DateTimeField(
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
    
    objects = ActiveShipmentManager()
    deleted_objects = DeletedShipmentManager()
    all_objects = AllShipmentManager()

    class Meta:
        ordering = ["-created_at"]
        

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["customer"]),
            models.Index(fields=["driver"]),
            models.Index(fields=["vehicle"]),
            models.Index(fields=["pickup_date"]),
            models.Index(fields=["estimated_delivery_date"]),
        ]

    def __str__(self):
        return self.shipment_number
    

class ShipmentStatusHistory(BaseModel, UUID):

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="status_history"
    )

    old_status = models.CharField(
        max_length=30
    )

    new_status = models.CharField(
        max_length=30
    )

    changed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="shipment_status_changes"
    )

    note = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.shipment.shipment_number}: "
            f"{self.old_status} → {self.new_status}"
        )
        

class ShipmentCharge(BaseModel, UUID):

    CHARGE_TYPE_CHOICES = [
        ("transportation", "Transportation"),
        ("loading", "Loading"),
        ("unloading", "Unloading"),
        ("handling", "Handling"),
        ("fuel", "Fuel"),
        ("toll", "Toll"),
        ("parking", "Parking"),
        ("other", "Other"),
    ]

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="charges"
    )

    charge_type = models.CharField(
        max_length=30,
        choices=CHARGE_TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    objects = ActiveShipmentChargeManager()
    deleted_objects = DeletedShipmentChargeManager()
    all_objects = AllShipmentChargeManager()

    def __str__(self):
        return f"{self.charge_type} - {self.amount}"
    
class IdempotancyKey(models.Model):
    key = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_idempotancy')
    response_data = models.JSONField(blank=True, null=True)
    status_code = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.key
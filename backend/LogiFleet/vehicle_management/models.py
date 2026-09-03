from django.db import models
from accounts.models import BaseModel
from customer_management.models import UUID
from .managers import ActiveVehicleManager, DeletedVehicleManager, AllVehicleManager


class Vehicle(BaseModel, UUID):

    VEHICLE_TYPE = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('trailer', 'Trailer'),
        ('other', 'Other'),
    ]

    FUEL_TYPE = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    VEHICLE_STATUS = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Maintenance'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired'),
    ]

    registration_number = models.CharField(
        max_length=50,
        unique=True
    )

    vin = models.CharField(
        max_length=100,
        unique=True
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE
    )

    make = models.CharField(
        max_length=100
    )

    model = models.CharField(
        max_length=100
    )

    year = models.PositiveIntegerField()

    capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE
    )

    current_mileage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=VEHICLE_STATUS,
        default='available'
    )

    purchase_date = models.DateField()
    
    is_deleted = models.BooleanField(default=False)
    
    objects = ActiveVehicleManager()
    deleted_objects = DeletedVehicleManager()
    all_objects = AllVehicleManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.registration_number} - {self.make} {self.model}"
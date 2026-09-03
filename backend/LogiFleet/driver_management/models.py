from django.db import models
from accounts.models import BaseModel
from customer_management.models import UUID
from .managers import ActiveDriverManagement, DeletedDriverManager, AllDriverManager

class Driver(BaseModel, UUID):
    
    DRIVER_STATUS = [
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('fire', 'Fire'),
    ]

    full_name = models.CharField(max_length=100, null=False)

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20
    )

    license_number = models.CharField(
        max_length=100,
        unique=True
    )

    license_type = models.CharField(
        max_length=50
    )

    license_expiry = models.DateField()

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=DRIVER_STATUS, default='active'
    )

    address = models.TextField(
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=20,
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
    
    objects = ActiveDriverManagement()
    deleted_objects = DeletedDriverManager()
    all_objects = AllDriverManager()
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.full_name} - {self.email}"
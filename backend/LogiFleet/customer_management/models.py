from django.db import models
from accounts.models import BaseModel
import uuid
from .managers import ActiveCustomerManager, DeletedCustomerManager, AllCustomerManager

class UUID(models.Model):
    code = models.CharField(max_length=200, unique=True, null=True, blank=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"UUID-{uuid.uuid4().hex[:8].upper()}"
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.code

# customer
class Customer(BaseModel, UUID):

    name = models.CharField(max_length=255, null=False)

    email = models.EmailField()
    
    phone = models.CharField(max_length=30, null=False)

    address = models.TextField()
    
    city = models.CharField(max_length=100)
    
    country = models.CharField(max_length=100)

    tax_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    credit_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )
    
    is_deleted = models.BooleanField(default=False)
    
    # managers
    objects = ActiveCustomerManager()
    deleted_objects = DeletedCustomerManager()
    all_objects = AllCustomerManager()
    
    def __str__(self):
        return f"{self.code}  {self.name}"
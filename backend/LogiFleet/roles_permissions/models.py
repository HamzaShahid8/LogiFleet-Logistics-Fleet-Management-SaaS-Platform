from django.db import models
from accounts.models import BaseModel

# Create your models here.

class Permissions(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.name
    
class Roles(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    permissions = models.ManyToManyField(Permissions)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.name